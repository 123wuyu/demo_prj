from flask import Flask
from redis.exceptions import RedisError
from sqlalchemy.exc import SQLAlchemyError
import grpc
from elasticsearch5 import Elasticsearch
import socketio
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor


def create_flask_app(config, enable_config_file=False):
    """
    创建Flask应用
    :param config: 配置信息对象
    :param enable_config_file: 是否允许运行环境中的配置文件覆盖已加载的配置信息
    :return: Flask应用
    """
    app = Flask(__name__)
    app.config.from_object(config)
    if enable_config_file:
        from utils import constants
        app.config.from_envvar(constants.GLOBAL_SETTING_ENV_NAME, silent=True)

    return app


def create_app(config, enable_config_file=False):
    """
    创建应用
    :param config: 配置信息对象
    :param enable_config_file: 是否允许运行环境中的配置文件覆盖已加载的配置信息
    :return: 应用
    """
    app = create_flask_app(config, enable_config_file)

    # 创建Snowflake ID worker
    from utils.snowflake.id_worker import IdWorker
    app.id_worker = IdWorker(app.config['DATACENTER_ID'],
                             app.config['WORKER_ID'],
                             app.config['SEQUENCE'])

    # 限流器
    from utils.limiter import limiter as lmt
    lmt.init_app(app)

    # 配置日志
    from utils.logging import create_logger
    create_logger(app)

    # 注册url转换器
    from utils.converters import register_converters
    register_converters(app)

    from redis.sentinel import Sentinel
    _sentinel = Sentinel(app.config['REDIS_SENTINELS'])
    app.redis_master = _sentinel.master_for(app.config['REDIS_SENTINEL_SERVICE_NAME'])
    app.redis_slave = _sentinel.slave_for(app.config['REDIS_SENTINEL_SERVICE_NAME'])

    from rediscluster import StrictRedisCluster
    app.redis_cluster = StrictRedisCluster(startup_nodes=app.config['REDIS_CLUSTER'])

    # rpc
    # 与推荐系统的rpc服务器连接
    app.rpc_reco = grpc.insecure_channel(app.config['RPC'].RECOMMEND)

    # Elasticsearch
    app.es = Elasticsearch(
        app.config['ES'],
        # sniff before doing anything
        sniff_on_start=True,
        # refresh nodes after a node fails to respond
        sniff_on_connection_fail=True,
        # and also every 60 seconds
        sniffer_timeout=60
    )

    # socket.io
    app.sio_mgr = socketio.KombuManager(app.config['RABBITMQ'], write_only=True)

    # MySQL数据库连接初始化
    from models import db

    db.init_app(app)

    # # 添加请求钩子
    from utils.middlewares import jwt_authentication
    app.before_request(jwt_authentication)

    # 注册用户模块蓝图
    from .resources.user import user_bp
    app.register_blueprint(user_bp)

    # 注册新闻模块蓝图
    from .resources.news import news_bp
    app.register_blueprint(news_bp)

    # 注册通知模块
    from .resources.notice import notice_bp
    app.register_blueprint(notice_bp)

    # 搜索
    from .resources.search import search_bp
    app.register_blueprint(search_bp)

    # apscheduler的使用
    # 创建调度器对象
    # 指明使用的执行器
    executors = {
        'default': ThreadPoolExecutor(20)
    }

    app.scheduler = BackgroundScheduler(executors=executors)

    # 此处添加 flask运行前就已经明确的定时任务
    # app.scheduler.add_job()
    # app.scheduler.add_job()

    # 定时修正统计数据的周期是 每天凌晨3点
    from .shedules.statistic import fix_statistics
    app.scheduler.add_job(fix_statistics, 'cron', hour=3, args=[app])

    # 为了测试需要立即看到效果
    # app.scheduler.add_job(fix_statistics, 'date', args=[app])

    # 注意，flask运行中 由视图产生的新定时任务 在视图中使用current_app.scheduler.add_job 完成

    app.scheduler.start()  # 非阻塞

    return app


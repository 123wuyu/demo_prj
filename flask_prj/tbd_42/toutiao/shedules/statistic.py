from sqlalchemy import func
from flask import current_app

from models import db
from models.news import Article
from cache import statistic as cache_statistic

# def fix_statistics(flask_app):
#     """
#     定时修正统计数据
#     :return:
#     """
#     # 注意此函数 是apscheduler在单独的子线程中执行，与flask执行请求和视图的流程无关，所有没有flask帮助
#     # 创建上下文环境，用到的current_app 需要自己手动为其创建应用上下文环境
#
#     with flask_app.app_context():
#
#         # 以用户文章数量为例
#         # 查询mysql数据库，统计所有用户的文章数量
#         # sql
#         # select user_id, count(article_id) from news_article_basic where status=2 group by user_id
#
#         ret = db.session.query(Article.user_id, func.count(Article.id)).filter(Article.status == Article.STATUS.APPROVED)\
#             .group_by(Article.user_id).all()
#
#         # +---------+-------------------+
#         # | user_id | count(article_id) |
#         # +---------+-------------------+
#         # |       1 |             46141 |
#         # |       2 |             46357 |
#         # |       3 |             46187 |
#         # |       5 |                25 |
#         # +---------+-------------------+
#
#         # ret -> [(1, 46141), (2, 46357), ...]
#
#         # 重置redis数据
#         r = current_app.redis_master
#
#         key = 'count:user:arts'
#
#         # 删除redis中原有数据
#         r.delete(key)
#
#         # 设置redis数据
#         #  zadd key score member
#
#         # 方式一：
#         # pl = r.pipeline()
#         # for user_id, count in ret:
#         #     pl.zadd(key, count, user_id)
#         #
#         # pl.execute()
#
#         # 方式二：
#         # #  zadd key score1 member1 score2 member2 score3 member3 ...
#
#         redis_data = []
#         for user_id, count in ret:
#             redis_data.append(count)
#             redis_data.append(user_id)
#
#         # redis_data ->  [count1, user_id1, count2, user_id2, ....]
#
#         r.zadd(key, *redis_data)
#         # r.zadd(key, count1, user_id1, count2, user_id2, ...)

# ********************************** 考虑到每个统计指标的修正都是类似的过程，复用代码 ********************

def __fix_process(storage_class):
    ret = storage_class.db_query()
    storage_class.reset(ret)


def fix_statistics(flask_app):
    """
    定时修正统计数据
    :return:
    """
    # 注意此函数 是apscheduler在单独的子线程中执行，与flask执行请求和视图的流程无关，所有没有flask帮助
    # 创建上下文环境，用到的current_app 需要自己手动为其创建应用上下文环境

    with flask_app.app_context():

        # 以用户文章数量为例
        # 查询mysql数据库，统计所有用户的文章数量
        # sql
        # select user_id, count(article_id) from news_article_basic where status=2 group by user_id
        # ret = cache_statistic.UserArticleCountStorage.db_query()
        #
        # # 重置redis数据
        # cache_statistic.UserArticleCountStorage.reset(ret)
        #
        #
        # ret = cache_statistic.UserFollowingCountStorage.db_query()
        # cache_statistic.UserFollowingCountStorage.reset(ret)

        __fix_process(cache_statistic.UserArticleCountStorage)
        __fix_process(cache_statistic.UserFollowingCountStorage)
        # __fix_process(cache_statistic.UserFansCountStorage)




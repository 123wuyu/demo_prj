from flask import g, current_app
from functools import wraps
from sqlalchemy.orm import load_only
from sqlalchemy.exc import SQLAlchemyError


from models import db


def set_db_to_read(func):
    """
    设置使用读数据库
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_read()
        return func(*args, **kwargs)
    return wrapper


def set_db_to_write(func):
    """
    设置使用写数据库
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_write()
        return func(*args, **kwargs)
    return wrapper


# 实现登录验证装饰器
def login_required(func):
    # 让被装饰器装饰的函数的属性不发生变化，主要是__name__属性。
    @wraps(func)
    def wrapper(*args,**kwargs):
        # 运行用户访问业务接口的条件：必须携带业务token
        # 如果用户携带了刷新token，不允许进入视图的业务逻辑。
        if g.user_id and g.is_refresh is False:
            return func(*args,**kwargs)
        else:
            # abort(403)
            return {'message':'Invalid token'},403
    # wrapper.__name__ = func.__name__
    return wrapper


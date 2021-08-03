from flask_restful import Resource
from flask import g

from utils.decorators import login_required
from cache import statistic as cache_statistic


class FigureResource(Resource):
    """
    用户统计数据
    """
    method_decorators = [login_required]

    def get(self):
        """
        获取用户统计数据
        """
        return {
            'fans_count': cache_statistic.UserFansCountStorage.get(g.user_id),
            'read_count': cache_statistic.UserArticlesReadingCountStorage.get(g.user_id)
        }

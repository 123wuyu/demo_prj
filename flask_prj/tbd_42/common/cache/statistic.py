from flask import current_app
from redis.exceptions import RedisError
from sqlalchemy import func

from models import db
from models.news import Article, Collection, Attitude, CommentLiking, Comment
from models.user import Relation

# 用户文章数量为例

#  key                     value
# count:user:arts          zset
#                       member   score
#                       user_id   article_count
#                           1       100
#                           2      10

# 需求
#   1. 查询用户文章数量
#   2. 数据累加
#
# 方式一
# class UserArticleCountStorage(object):
#     """
#     用户文章数量 工具类
#     """
#     key = 'count:user:arts'
#
#     def __init__(self, user_id):
#         self.user_id = user_id
#
#     def get(self):
#         key  user_id
#
#
#     def incr(self):
# user1   UserArticleCountStorage(1)   key='count:user:arts'
# user2   UserArticleCountStorage(2)   key='count:user:arts'

#
# # 方式二
# class UserArticleCountStorage(object):
#     """
#     用户文章数量 工具类
#     """
#     key = 'count:user:arts'
#
#     @classmethod
#     def get(cls, user_id):
#         """
#         查询用户的文章数量
#         :param user_id:
#         :return:
#         """
#         # 查询redis
#         try:
#             ret = current_app.redis_master.zscore(cls.key, user_id)
#         except RedisError as e:
#             current_app.logger.error(e)
#             ret = current_app.redis_slave.zscore(cls.key, user_id)
#
#         # 返回
#         return 0 if ret is None else int(ret)
#
#     @classmethod
#     def incr(cls, user_id, increment=1):
#         """
#         累加数量
#         :param user_id:
#         :param increment: 增量 可正可负
#         :return:
#         """
#         try:
#             current_app.redis_master.zincrby(cls.key, increment, user_id)
#         except RedisError as e:
#             current_app.logger.error(e)
#             raise e
#
#
# # user1  UserArticleCountStorage.get(1)  UserArticleCountStorage.incr(1)  UserArticleCountStorage.incr(1， -2)
# # user2  UserArticleCountStorage.get(2)

##################### 考虑到每个统计指标的数据维护工具 操作方式都相同 ，所以复用代码##############################################

class CountStorageBase(object):
    """
    统计数量工具类父类
    """
    key = ''

    @classmethod
    def get(cls, member_id):
        """
        查询数量
        :param member_id:   可能是用户的id 或者 文章的id
        :return:
        """
        # 查询redis
        try:
            ret = current_app.redis_master.zscore(cls.key, member_id)
        except RedisError as e:
            current_app.logger.error(e)
            ret = current_app.redis_slave.zscore(cls.key, member_id)

        # 返回
        return 0 if ret is None else int(ret)

    @classmethod
    def incr(cls, member_id, increment=1):
        """
        累加数量
        :param member_id:
        :param increment: 增量 可正可负
        :return:
        """
        try:
            current_app.redis_master.zincrby(cls.key, increment, member_id)
        except RedisError as e:
            current_app.logger.error(e)
            raise e

    @classmethod
    def reset(cls, db_query_result):
        """
        重置redis记录，是定时任务调用的
        :return:
        """
        r = current_app.redis_master

        # 删除redis中原有数据
        r.delete(cls.key)

        # 设置redis数据
        #  zadd key score member

        # 方式一：
        # pl = r.pipeline()
        # for user_id, count in ret:
        #     pl.zadd(key, count, user_id)
        #
        # pl.execute()

        # 方式二：
        # #  zadd key score1 member1 score2 member2 score3 member3 ...

        redis_data = []
        for user_id, count in db_query_result:
            redis_data.append(count)
            redis_data.append(user_id)

        # redis_data ->  [count1, user_id1, count2, user_id2, ....]

        r.zadd(cls.key, *redis_data)
        # r.zadd(key, count1, user_id1, count2, user_id2, ...)

    @staticmethod
    def db_query():
        """
        统计数据对应的数据库mysql查询，供定时任务使用
        :return:
        """
        pass


class UserArticleCountStorage(CountStorageBase):
    """
    用户文章数量 工具类
    """
    key = 'count:user:arts'

    @staticmethod
    def db_query():
        ret = db.session.query(Article.user_id, func.count(Article.id)).filter(
            Article.status == Article.STATUS.APPROVED) \
            .group_by(Article.user_id).all()

        return ret


class UserFollowingCountStorage(CountStorageBase):
    """
    用户关注数量 工具类
    """
    key = 'count:user:following'

    @staticmethod
    def db_query():
        # sql
        # select user_id, count(target_user_id) from user_relation where relation=1 group by user_id
        return db.session.query(Relation.user_id, func.count(Relation.target_user_id))\
            .filter(Relation.relation == Relation.RELATION.FOLLOW).group_by(Relation.user_id).all()


class UserFansCountStorage(CountStorageBase):
    """
    用户粉丝数量 工具类
    """
    key = 'count:user:fans'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Relation.target_user_id, func.count(Relation.user_id)) \
            .filter(Relation.relation == Relation.RELATION.FOLLOW) \
            .group_by(Relation.target_user_id).all()
        return ret


class UserLikingCountStorage(CountStorageBase):
    """
    用户点赞数量 工具类
    """
    key = 'count:user:liking'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Article.user_id, func.count(Attitude.id)).join(Attitude.article) \
            .filter(Attitude.attitude == Attitude.ATTITUDE.LIKING) \
            .group_by(Article.user_id).all()
        return ret


class ArticleReadingCountStorage(CountStorageBase):
    """
    文章阅读量
    """
    key = 'count:art:reading'


class UserArticlesReadingCountStorage(CountStorageBase):
    """
    作者的文章阅读总量
    """
    kye = 'count:user:arts:reading'


class ArticleCollectingCountStorage(CountStorageBase):
    """
    文章收藏数量
    """
    key = 'count:art:collecting'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Collection.article_id, func.count(Collection.article_id)) \
            .filter(Collection.is_deleted == 0).group_by(Collection.article_id).all()
        return ret


class UserArticleCollectingCountStorage(CountStorageBase):
    """
    用户收藏数量
    """
    key = 'count:user:art:collecting'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Collection.user_id, func.count(Collection.article_id)) \
            .filter(Collection.is_deleted == 0).group_by(Collection.user_id).all()
        return ret


class ArticleDislikeCountStorage(CountStorageBase):
    """
    文章不喜欢数据
    """
    key = 'count:art:dislike'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Attitude.article_id, func.count(Collection.article_id)) \
            .filter(Attitude.attitude == Attitude.ATTITUDE.DISLIKE).group_by(Collection.article_id).all()
        return ret


class ArticleLikingCountStorage(CountStorageBase):
    """
    文章点赞数据
    """
    key = 'count:art:liking'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Attitude.article_id, func.count(Collection.article_id)) \
            .filter(Attitude.attitude == Attitude.ATTITUDE.LIKING).group_by(Collection.article_id).all()
        return ret


class CommentLikingCountStorage(CountStorageBase):
    """
    评论点赞数据
    """
    key = 'count:comm:liking'

    @classmethod
    def db_query(cls):
        ret = db.session.query(CommentLiking.comment_id, func.count(CommentLiking.comment_id)) \
            .filter(CommentLiking.is_deleted == 0).group_by(CommentLiking.comment_id).all()
        return ret


class ArticleCommentCountStorage(CountStorageBase):
    """
    文章评论数量
    """
    key = 'count:art:comm'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Comment.article_id, func.count(Comment.id)) \
            .filter(Comment.status == Comment.STATUS.APPROVED).group_by(Comment.article_id).all()
        return ret


class CommentReplyCountStorage(CountStorageBase):
    """
    评论回复数量
    """
    key = 'count:art:reply'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Comment.parent_id, func.count(Comment.id)) \
            .filter(Comment.status == Comment.STATUS.APPROVED, Comment.parent_id != None)\
            .group_by(Comment.parent_id).all()
        return ret


class UserLikedCountStorage(CountStorageBase):
    """
    用户被赞数量
    """
    key = 'count:user:liked'

    @classmethod
    def db_query(cls):
        ret = db.session.query(Article.user_id, func.count(Attitude.id)).join(Attitude.article) \
            .filter(Attitude.attitude == Attitude.ATTITUDE.LIKING) \
            .group_by(Article.user_id).all()
        return ret

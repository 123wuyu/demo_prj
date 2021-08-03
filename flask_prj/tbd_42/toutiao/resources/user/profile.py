# 导入g对象
from flask import g,current_app
# 导入扩展包flask-restful提供的基类，校验参数的工具类
from flask_restful import Resource,reqparse

# 导入检查文件是否是图片的工具函数
from utils.parser import check_image
# 导入登录验证装饰器
from utils.decorators import login_required
# 导入七牛云的工具
from utils.qiniu_storage import upload
# 导入模型类
from models.user import User
from models import db
from cache import user as cache_user  # 起别名
from cache import statistic as cache_statistic


# 定义视图类，处理用户头像
class PhotoResource(Resource):

    method_decorators = [login_required]

    def patch(self):
        # 接收参数
        # 校验参数
        req = reqparse.RequestParser()
        req.add_argument('photo',type=check_image,required=True,location='files')
        args = req.parse_args()
        image = args.get("photo")
        # 业务处理
        # 上传头像
        data = image.read()
        try:
            image_name = upload(data)
        except Exception as e:
            current_app.logger.error(e)
            return {'message':'server error'},500
        # 需要保存用户头像
        # User.query.get(g.user_id)
        # User.query.filter(User.is==g.user_id).update({'profile_photo':image_name})
        # db.session.commit()
        try:
            user = User.query.filter_by(id=g.user_id).first()
            user.profile_photo = image_name
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            # flask-sqlalchemy自带事务，可以不用手动回滚。
            # db.session.rollback()
        # 返回结果
        photo_url = current_app.config.get("QINIU_DOMAIN") + image_name
        return {'photo_url':photo_url}
        pass


# /users/123
# /users/<int(min=1):user_id>
class UserResource(Resource):
    """
    用户信息接口
    """
    def get(self, user_id):
        # 检验参数
        cache_tool = cache_user.UserProfileCache(user_id)
        if not cache_tool.exists():
            # 用户不存在
            return {'message': 'Invalid user_id'}, 404

        # 业务处理
        # 查询用户数据
        user_dict = cache_tool.get()

        # 返回
        # {
        # 	"message": "OK",
        # 	"data": {
        # 		"user_id": xxx,
        # 		"name": xx,
        # 		"photo": xx,
        # 		"certi": xxx,
        # 		"intro": xx,
        # 		"article_count": xx,
        # 		"follow_count": xx,
        # 		"fans_count": xx,
        # 		"liking_count": xx
        # 	}
        # }

        user_dict['user_id'] = user_id
        del user_dict['mobile']
        user_dict['photo'] = current_app.config['QINIU_DOMAIN'] + user_dict['photo']

        user_dict['article_count'] = cache_statistic.UserArticleCountStorage.get(user_id)
        user_dict['follow_count'] = cache_statistic.UserFollowingCountStorage.get(user_id)
        user_dict['fans_count'] = cache_statistic.UserFansCountStorage.get(user_id)
        user_dict['liking_count'] = cache_statistic.UserLikingCountStorage.get(user_id)

        return user_dict


class CurrentUserResource(Resource):
    """
    用户自己的数据
    """
    method_decorators = [login_required]

    def get(self):
        """
        获取当前用户自己的数据
        """
        user_data = cache_user.UserProfileCache(g.user_id).get()
        user_data['id'] = g.user_id
        del user_data['mobile']
        return user_data


class ProfileResource(Resource):
    """
    用户资料
    """
    method_decorators = {
        'get': [login_required],
    }

    def get(self):
        """
        获取用户资料
        """
        user_id = g.user_id
        user = cache_user.UserProfileCache(user_id).get()
        result = {
            'id': user_id,
            'name': user['name'],
            'photo': user['photo'],
            'mobile': user['mobile']
        }
        # 补充性别生日等信息
        result.update(cache_user.UserAdditionalProfileCache(user_id).get())
        return result

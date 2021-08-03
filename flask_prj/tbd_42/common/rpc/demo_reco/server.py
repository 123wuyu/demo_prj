import grpc
from concurrent.futures import ThreadPoolExecutor
import time

import reco_pb2_grpc
import reco_pb2


# 补全被调用的代码
class UserRecommendServicer(reco_pb2_grpc.UserRecommendServicer):
    def user_recommend(self, request, context):
        """

        :param request:  rpc调用请求 此处是UserRequest类的对象
        :param context:  用来返回函数调用的异常信息， 可以设置状态码和异常信息
                context.set_code(grpc.StatusCode.UNIMPLEMENTED)
                context.set_details('Method not implemented!'
        :return:
        """
        # 此处应该编写的是rpc被调用的业务代码
        # 实际上此处是应该有推荐系统人员编写
        # 编写推荐代码
        # 为了测试rpc流程，编写测试的推荐代码

        # 获取rpc调用请求的参数
        user_id = request.user_id
        channel_id = request.channel_id
        article_num = request.article_num
        time_stamp = request.time_stamp

        # 构造rpc调用的返回值
        response = reco_pb2.ArticleResponse()
        response.exposure = 'exposure param'
        response.time_stamp = round(time.time() * 1000)

        articles = []
        for i in range(article_num):
            article = reco_pb2.Article()
            article.article_id = i + 1
            article.track.click = 'click param'
            article.track.collect = 'collect param'
            article.track.share = 'share param'
            article.track.read = 'read param'

            articles.append(article)

        response.recommends.extend(articles)
        return response


# 编写rpc服务器运行代码
def serve():
    # 创建rpc服务器对象
    server = grpc.server(ThreadPoolExecutor(max_workers=20))

    # 为rpc服务器 注册能够对外提供的代码
    reco_pb2_grpc.add_UserRecommendServicer_to_server(UserRecommendServicer(), server)

    # 绑定rpc ip地址和端口号
    server.add_insecure_port('127.0.0.1:8888')

    # 启动服务器
    server.start()  # 非阻塞

    # 为了防止程序因为非阻塞退出，手动阻塞
    while True:
        time.sleep(10)


if __name__ == '__main__':
    serve()


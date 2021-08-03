import grpc
import time

import reco_pb2_grpc
import reco_pb2


def run():
    # 连接rpc服务器 得到与rpc连接的对象
    with grpc.insecure_channel('127.0.0.1:8888') as conn:
        # 创建进行rpc调用的工具对象
        stub = reco_pb2_grpc.UserRecommendStub(conn)

        # 通过工具对象 进行rpc函数调用
        req = reco_pb2.UserRequest()
        req.user_id = '1'
        req.channel_id = 12
        req.article_num = 10
        req.time_stamp = round(time.time() * 1000)

        ret = stub.user_recommend(req)
        # ret -> ArticleResponse 对象
        print(ret)


if __name__ == '__main__':
    run()

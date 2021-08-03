import grpc
from concurrent.futures import ThreadPoolExecutor
import time

import calculate_pb2_grpc
import calculate_pb2


class CalculateServicer(calculate_pb2_grpc.CalculateServicer):
    def add(self, request, context):
        """

        :param request: 调用函数的传入参数  （num1 num2) 是Nums类的对象
        :param context:
        :return:
        """
        num1 = request.num1
        num2 = request.num2

        result = num1 + num2

        sum_obj = calculate_pb2.Sum()
        sum_obj.result = result

        return sum_obj


# 编写rpc服务器运行代码
def serve():
    # 创建rpc服务器对象
    server = grpc.server(ThreadPoolExecutor(max_workers=20))

    # 为rpc服务器 注册能够对外提供的代码
    calculate_pb2_grpc.add_CalculateServicer_to_server(CalculateServicer(), server)

    # 绑定rpc ip地址和端口号
    server.add_insecure_port('127.0.0.1:8888')

    # 启动服务器
    server.start()  # 非阻塞

    # 为了防止程序因为非阻塞退出，手动阻塞
    while True:
        time.sleep(10)


if __name__ == '__main__':
    serve()
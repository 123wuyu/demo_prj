import grpc
import calculate_pb2_grpc
import calculate_pb2


with grpc.insecure_channel('127.0.0.1:8888') as conn:

    stub = calculate_pb2_grpc.CalculateStub(conn)

    nums_obj = calculate_pb2.Nums()
    nums_obj.num1 = 100
    nums_obj.num2 = 200

    sum_obj = stub.add(nums_obj)

    # sum_obj -> Sum 对象
    print(sum_obj.result)
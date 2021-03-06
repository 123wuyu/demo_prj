# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import calculate_pb2 as calculate__pb2


class CalculateStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.add = channel.unary_unary(
        '/Calculate/add',
        request_serializer=calculate__pb2.Nums.SerializeToString,
        response_deserializer=calculate__pb2.Sum.FromString,
        )


class CalculateServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def add(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_CalculateServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'add': grpc.unary_unary_rpc_method_handler(
          servicer.add,
          request_deserializer=calculate__pb2.Nums.FromString,
          response_serializer=calculate__pb2.Sum.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Calculate', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

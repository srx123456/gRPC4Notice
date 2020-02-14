from concurrent import futures
import logging

import grpc

import hello_pb2
import hello_pb2_grpc

from src.hello import Hello

def serve():
    print('starting server..')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServicer_to_server(Hello(), server)
    server.add_insecure_port('[::]:50051')
    print('started server on http://localhost:50051')
    server.start()
    server.wait_for_termination()



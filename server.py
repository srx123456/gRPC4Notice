from concurrent import futures
import logging

import grpc
import json

import path_pb2
import path_pb2_grpc

from src.path import Path
from util.JsonOperator import getConf

def serve():
    print('starting server..')
    exploreInfo = getConf()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    path_pb2_grpc.add_PathServicer_to_server(Path(), server)
    server.add_insecure_port('[::]:'+str(exploreInfo.control_port))
    # print('started server on http://localhost:50051')
    server.start()
    server.wait_for_termination()

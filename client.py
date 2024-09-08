from __future__ import print_function
import logging
import threading
import time
import grpc

from io import BytesIO, open
from src.ExploreFormat import ExploreFormat

import path_pb2
import path_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = path_pb2_grpc.PathStub(channel)
        
        request = path_pb2.PathRequest(
            instance_id=123,
            control_param=1,
            service_type=2,
            instance_status=3,
            instance_version=1,
            service_dest_address="192.168.1.1",
            current_hop_count=1,
            max_hop_count=10,
            ttl=3600,
            heartbeat_msg=0,
            extension=b'example_extension'
        )
        
        # 调用 Greet 方法并接收单一的 PathResponse 对象
        response = stub.Greet(request)
        
        # 直接打印响应对象
        print(f'Received response: {response}')
        # 追加发包程序

if __name__ == '__main__':
    logging.basicConfig()
    run()
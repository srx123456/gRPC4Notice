from __future__ import print_function
import logging
import grpc
from io import BytesIO, open
from util.JsonOperator import getConf

import path_pb2
import path_pb2_grpc

def run():
    exploreInfo = getConf()
    with grpc.insecure_channel('localhost'+':'+str(exploreInfo.control_port)) as channel:
        stub = path_pb2_grpc.PathStub(channel)
        
        request = path_pb2.PathRequest(
            instance_id=exploreInfo.instance_id,
            control_param=exploreInfo.control_param,
            service_type=exploreInfo.service_type,
            instance_status=exploreInfo.instance_state,
            instance_version=exploreInfo.instance_version,
            service_dest_address=exploreInfo.destination_address,
            current_hop_count=exploreInfo.current_hop,
            max_hop_count=exploreInfo.max_hop,
            ttl=exploreInfo.ttl,
            heartbeat_msg=exploreInfo.heartbeat,
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
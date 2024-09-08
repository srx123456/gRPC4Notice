import random
import subprocess
import grpc
import socket
import re
import os
import json
from os import path

import path_pb2
import path_pb2_grpc
from src.InfoCollection import PortGet
from src.PathSelect import RandomSelect
from util.JsonOperator import load_sorWeight,getConf

class Path(path_pb2_grpc.PathServicer):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录
    SOR_FILE_NAME = os.path.join(base_dir, '..', 'data', 'SORInfo.txt')

    def get_own_ip(self):
        # 获取当前节点IP
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

    def get_valid_next_address(self, client_ip):
        # 获取所有可用SOR节点信息
        sorWeight = load_sorWeight(self.SOR_FILE_NAME)
        keys = list(sorWeight.keys())
        server_ip = self.get_own_ip()
        print(f"Server IP: {server_ip}")
        # valid_addresses = [ip for ip in sorWeight['valid_addresses'] if ip != server_ip and ip != client_ip]
        valid_addresses = [ip for ip in keys if ip != server_ip]

        # 随机选择一个 非上一跳 非当前 的SOR节点
        if valid_addresses:
            return RandomSelect.select_best_individuals(valid_addresses, 1) 
        else:
            raise Exception("No valid next address available")
    
    # 目前是ipv6地址
    def get_client_from_RPC(self, context):
        # 从 gRPC 中获取客户端 IP
        peer = context.peer()
        print(peer)
        # 提取 IP 地址
        ipv4_pattern = re.compile(r'ipv4:([\d.]+)')
        ipv6_pattern = re.compile(r'ipv6:\[([^\]]+)\]')

        # 检查 IPv4
        match = ipv4_pattern.search(peer)
        if match:
            client_ip = match.group(1)
        else:
            # 检查 IPv6
            match = ipv6_pattern.search(peer)
            if match:
                # 如果需要，可以在此处将 IPv6 转换为 IPv4
                client_ip = match.group(1)
            else:
                # 默认处理
                client_ip = peer.split(":")[1].strip()
        return client_ip

    def Greet(self, request, context):
        # 更新 current_hop_count
        new_current_hop = request.current_hop_count + 1
        # 获取数据控制端口
        exploreInfo = getConf()
        # 设置remote 转发地址
        RemoteIP = request.service_dest_address
        RemotePort = 12333
        #  从gRPC中获取上一跳IP
        client_ip = self.get_client_from_RPC(context)
        # 处理接收到的请求数据
        # 设置返回端口和返回地址
        # return_port = PortGet.get_my_available_port()
        return_port = random.randint(46888, 65535)
        try:
            next_address = self.get_valid_next_address(client_ip)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Error selecting next address: {str(e)}')
            return
        print(f"Client IP: {client_ip}")
        print(f"next IP: {next_address}")

        try:
            response = path_pb2.PathResponse(
                instance_id=request.instance_id,
                control_param=request.control_param,
                service_type=request.service_type,
                instance_status=request.instance_status,
                instance_version=request.instance_version,
                service_dest_address=request.service_dest_address,
                current_hop_count=request.current_hop_count,
                max_hop_count=request.max_hop_count,
                ttl=request.ttl,
                heartbeat_msg=request.heartbeat_msg,
                return_port=return_port,
                return_address=self.get_own_ip(),  
                extension=request.extension
            )
            # print(f'Constructed response: {response}')
        except Exception as e:
            print(f'Error in Greet method: {str(e)}')
            context.set_details(f'Error: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)

        new_request = path_pb2.PathRequest(
            instance_id=request.instance_id,
            control_param=request.control_param,
            service_type=request.service_type,
            instance_status=request.instance_status,
            instance_version=request.instance_version,
            service_dest_address=request.service_dest_address,
            current_hop_count=new_current_hop,
            max_hop_count=request.max_hop_count,
            ttl=request.ttl,
            heartbeat_msg=request.heartbeat_msg,
            extension=request.extension
        )

        # 如果 current_hop_count < 3, 转发到下一跳 next_address'localhost:50051'
        if new_current_hop < 3:
            with grpc.insecure_channel('localhost'+':'+str(exploreInfo.control_port)) as channel:
                stub = path_pb2_grpc.PathStub(channel)
                responses = stub.Greet(new_request)
                RemoteIP = responses.return_address
                RemotePort = responses.return_port
                print(f'Forwarded request to next server: {responses}')
        
        LocalIP = self.get_own_ip()
        LocalPort = return_port
        # 运行转发程序
        # command = f'/tinymapper -l'+LocalIP+':'+str(LocalPort)+' -r'+RemoteIP+':'+str(RemotePort) +'-u'
        # subprocess.run(command, shell=True, text=True, capture_output=True)
        print(f'/tinymapper -l'+LocalIP+':'+str(LocalPort)+' -r'+RemoteIP+':'+str(RemotePort) +'-u')

        return response

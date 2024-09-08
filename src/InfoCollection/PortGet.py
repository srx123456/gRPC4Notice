import subprocess
import re
import random

def get_my_available_port():
    # 执行netstat命令获取端口信息
    output = subprocess.check_output(['netstat', '-tuln'], universal_newlines=True)
    # 使用正则表达式匹配端口号
    port_pattern = r':(\d+)'
    ports = re.findall(port_pattern, output)
    # 随机选择一个端口号
    port = random.randint(46888, 65535)
    # 检查随机选择的端口是否已被占用
    while str(port) in ports:
        port = random.randint(46888, 65535)
    return port
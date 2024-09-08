import json
import sys

from src.ExploreFormat import ExploreFormat

# 文件路径
CONFIG_FILE_PATH = 'data\config.json'

def load_sorWeight(filepath):
    # 如果没有这个属性，就初始化它
    if not hasattr(load_sorWeight, "call_count"):
        load_sorWeight.call_count = 0
    # 增加调用次数
    load_sorWeight.call_count += 1
    print(f"Function called {load_sorWeight.call_count} times")

    with open(filepath, 'r', encoding='utf-8') as f:
        sorMsg = json.load(f)
    sorWeight = {}
    for key, value in sorMsg.items():
        sorWeight[key] = [float(x.split(':')[1]) for x in value.split(',')]     
    return sorWeight

def update_sorWeight(best_individuals, filepath='data/totalMsgFile.txt'):
    with open(filepath, 'r') as f:
        sorMsg = json.load(f)

    for ind in best_individuals:
        key = list(ind.keys())[0]
        values = sorMsg[key].split(',')
        updated_values = []
        for v in values:
            param, val = v.split(':')
            if float(val) > 0.99:
                print("Value exceeds 0.99, exiting program.")
                sys.exit(1)
            updated_val = float(val) + 0.10  # Increment the value by 0.1
            updated_values.append(f"{param}:{updated_val}")
        sorMsg[key] = ','.join(updated_values)

    with open(filepath, 'w') as f:
        json.dump(sorMsg, f, indent=4)


def update_sorWeightRandom(best_individuals, filepath='data/totalMsgFile.txt'):
    with open(filepath, 'r') as f:
        sorMsg = json.load(f)

    for ind in best_individuals:
        values = sorMsg[ind].split(',')
        updated_values = []
        for v in values:
            param, val = v.split(':')
            if float(val) > 0.99:
                print("Value exceeds 0.99, exiting program.")
                sys.exit(1)
            updated_val = float(val) + 0.10  # Increment the value by 0.1
            updated_values.append(f"{param}:{updated_val}")
        sorMsg[ind] = ','.join(updated_values)

    with open(filepath, 'w') as f:
        json.dump(sorMsg, f, indent=4)

def getConf():
    # 读取并解析 JSON 文件
    try:
        with open(CONFIG_FILE_PATH, 'r') as file:
            # 读取文件内容
            file_content = file.read()
            # 解析 JSON 数据
            data = json.loads(file_content)
            
            # 访问具体字段
            control_port = data.get('control_port')
            instance_id = data.get('instance_id')
            control_param = data.get('control_param')
            service_type = data.get('service_type')
            instance_status = data.get('instance_status')
            instance_version = data.get('instance_version')
            service_dest_address = data.get('service_dest_address')
            current_hop_count = data.get('current_hop_count')
            max_hop_count = data.get('max_hop_count')
            ttl = data.get('ttl')
            heartbeat_msg = data.get('heartbeat_msg')
            extension = data.get('extension')

            return ExploreFormat(instance_id,control_param,service_type,instance_status,instance_version,service_dest_address,
                                 current_hop_count,max_hop_count,ttl,heartbeat_msg,0,"",extension,control_port)
    except FileNotFoundError:
        print(f"File not found: {CONFIG_FILE_PATH}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
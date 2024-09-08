import json
import sys

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
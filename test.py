from src.PathSelect import RandomSelect
from util.JsonOperator import load_sorWeight

# 获取所有可用SOR节点信息
sorWeight = load_sorWeight('data/SORInfo.txt' )
print(f"All IP: {sorWeight}")

# 随机选择一个 非上一跳 非当前 的SOR节点
if sorWeight:
    print(RandomSelect.select_best_individuals(sorWeight, 1))
else:
    raise Exception("No valid next address available")
    

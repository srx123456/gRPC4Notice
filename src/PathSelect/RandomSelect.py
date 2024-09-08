import random
from util.JsonOperator import load_sorWeight

def select_best_individuals(keys, k=3):
    if len(keys) < k:
        raise ValueError("Not enough nodes to select from.")
    best_individuals = random.sample(keys, k)
    return ', '.join(str(x) for x in best_individuals)

# 示例主函数
def main():
    file_path = '../data/SORInfo.txt' 
    sorWeight = load_sorWeight(file_path)
    
    best_individuals = select_best_individuals(sorWeight, 1)
    print(best_individuals)

if __name__ == "__main__":
    while(True):
        main()

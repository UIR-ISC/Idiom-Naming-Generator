import torch
import random
# 成语字随机替换函数，返回替换的成语位置
def random_replace(num):
    '''
    后续可以在里面填充其他替换函数
    '''
    randnum=torch.rand(1,num)
    print("randnum:",randnum)
    position=torch.argmax(randnum).item()
    print("position:",position)
    return position

def random_list(a,b,num):
    #生成随机数串
    # random.seed(100)
    L1=random.sample(range(a,b),num)
    return L1

if __name__ == '__main__':
    print(random_list(1,988,50))
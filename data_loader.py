# 读取拼音-汉字和拼音-单词键值对（字典格式）
import pandas as pd
import json
#拼音：谐音字
def dict_hom_char():
    '''可以改写成一个读入函数'''
    with open('data/hom_char.json','r') as f:
        hom_char=json.load(f)
    return hom_char
#拼音：谐音词
def dict_hom_word():
    with open('data/hom_word.json','r') as f:
        hom_word=json.load(f)
    return hom_word

if __name__ == '__main__':
    with open('data/苏菜_2.csv','r',encoding='utf8') as f:
        data=f.readlines()
    data=data[1:]
    for item in data:
        print(item.split('\t'))
    # data = pd.read_csv('data/苏菜_2.csv')
    # topics = data['名称'].tolist()
    # descriptions = data['名称'] + data['评价']
    # descriptions = descriptions.tolist()
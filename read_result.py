import json
from icecream import ic


with open('result.txt','r',encoding='utf8') as f:
    result=f.read()
    result=json.loads(result)
ic(result)

import pandas as pd
#删除索引指定列
# data=pd.read_csv('data/simplified_idioms_lazypinyin.csv')[:10]
# print(data)
# data=data.drop(data[data.idiom=='坚定不移'].index)
# print(data)
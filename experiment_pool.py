# -*- coding: utf-8 -*-
#尝试随机谐音替换
import torch
import json
import pandas as pd
from pypinyin import pinyin,lazy_pinyin
from tqdm import tqdm


randnum=torch.rand(1,4)
print(randnum)
print(torch.argmax(randnum).item())

with open('../Homophony/hom_char.json','r') as f:
    hom_char=json.load(f)
# hom_char键值对对应为拼音-对应的文字

with open('../Homophony/hom_word.json','r') as f:
    hom_word=json.load(f)
# hom_word
#打开成语词典的语料集
idioms=pd.read_csv('../Homophony/simplified_idioms.csv')
# print(idioms.head())

# a=pinyin('坚定不移')
# b=lazy_pinyin("坚定不移")
# print(a,b)

# df.iloc[行数,df.columns.get_loc(列名)]=new_value
for i in range(len(idioms)):
    idioms.iloc[i,idioms.columns.get_loc('pinyin')]=lazy_pinyin(idioms['idiom'][i])

#检索含有椰子的ye的成语
filter_idioms=pd.DataFrame(columns=['idiom','pinyin','explanation'])
for i in range(len(idioms)):
    data=idioms.loc[i]
#     print(type(data))
#     print(data['pinyin'])
#     break
    if 'ka' in data['pinyin']:#ye
        data=data.to_frame()
        data=data.T#必须要赋值
        # print(data.columns)
#         break
        filter_idioms=pd.concat([filter_idioms,data])

# print(filter_idioms)

idioms_demo=filter_idioms['idiom'].tolist()
pinyin_demo=filter_idioms['pinyin'].tolist()
explanation_demo=filter_idioms['explanation'].tolist()
# pinyin_demo[0].index('ye'),idioms_demo[0][3]

modify_idioms=[]
# idioms_demo[0].replace(idioms_demo[0][pinyin_demo[0].index('ye')],'椰')

for i in range(len(idioms_demo)):
    str1=idioms_demo[i].replace(idioms_demo[i][pinyin_demo[i].index('ka')],'咖')
    modify_idioms.append(str1)
# print(modify_idioms,len(modify_idioms))
# print(explanation_demo,len(explanation_demo))

#进行语义匹配尝试
from sentence_transformers import SentenceTransformer,util
model=SentenceTransformer('paraphrase-distilroberta-base-v1')
#对所有的对应生成的成语语义进行编码
# sentence=explanation_demo

embedding=model.encode(explanation_demo)
#对所有生成的成语直接进行编码处理
# embedding=model.encode(modify_idioms)
# embedding=model.encode(modify_idioms)
#计算与描述相关的相似度
# description='椰树牌椰汁是以海南盛产的椰子为原料，28年坚持在海南岛用新鲜椰子肉鲜榨，采用先进的加工技术及科学配方精制而成。它是一种不加香精、糖精、防腐剂不含胆固醇的天然植物蛋白饮料，其汁液均匀乳白、清醇，具有浓郁的天然椰香味，口感柔和、甜度适中、含有脂肪、蛋白质、十七种氨基酸和锌、铁、钙、锰等元素。于1991年被定为中国国宴饮料，产品畅销全国，远销世界33个国家和地区。'
description="蓝山咖啡，是指由产自牙买加蓝山的咖啡豆冲泡而成的咖啡。其中依档次又分为牙买加蓝山咖啡和牙买加高山咖啡。蓝山山脉位于牙买加岛（Jamaica） 东部，因该山在加勒比海的环绕下，每当天气晴朗的日子，太阳直射在蔚蓝的海面上，山峰上反射出海水璀璨的蓝色光芒，故而得名。蓝山最高峰海拔2256米，是加勒比地区的最高峰，也是著名的旅游胜地。这里地处地震带，拥有肥沃的火山土壤，空气清新，没有污染，气候湿润，终年多雾多雨，（平均降水为1980毫米，气温在27度左右）这样的气候造就了享誉世界的牙买加蓝山咖啡，同时也造就了世界上价格第二高的咖啡。此种咖啡拥有所有好咖啡的特点，不仅口味浓郁香醇，而且由于咖啡的甘、酸、苦三味搭配完美，所以完全不具苦味，仅有适度而完美的酸味。"
cos_sim=util.pytorch_cos_sim(model.encode(description),embedding)
print(cos_sim)
all_sentence_combinations=[]
for i in range(len(cos_sim[0])):
    # print(cos_sim[0][i])
    all_sentence_combinations.append([cos_sim[0][i],i])
print(all_sentence_combinations)
all_sentence_combinations=sorted(all_sentence_combinations,key=lambda x:x[0],reverse=True)
print("Top-10 most similar pairs:")
for score,i in all_sentence_combinations[0:10]:
    print(score,i)
    print("{} \t {} \t {:.4f}".format(modify_idioms[i],explanation_demo[i],cos_sim[0][i]))





#coding=utf-8
import torch
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import hanlp
import logging
from save_log import Logger
from icecream import ic
from keywords_extractor import extract_keywords
from exchange_idioms import main_replace
from sbert_sort import Sbert_sort
from edit_distance import editdistance
import sys
from random_place import *
from mixed_sort import *
#没考虑到前后鼻音chen和cheng

def main(topic,description,pos_tagger,tokenizer,model):
    keywords = extract_keywords(description, topic,pos_tagger)
    ic(keywords)
    if len(keywords)==0:#bug:针对没有检测出关键词
        keywords=[topic[-1]]
    exchanged_idioms = main_replace(keywords)
    ic(exchanged_idioms)
    if len(exchanged_idioms) == 0:
        result=['未找到可替换成语']
        return result
    if len(exchanged_idioms)>10:
        score1=editdistance(exchanged_idioms, description,tokenizer)#使用成语和其的编辑距离
        score=[item[0] for item in score1[:10]]
        print(score)
        exchanged_idioms=exchanged_idioms[exchanged_idioms.modified_idioms.isin(score)]
    #使用SBert进行排序
    # result,_ = Sbert_sort(model,exchanged_idioms, description)
    #使用mixed算法进行排序
    result,_=mix_sort(model,exchanged_idioms,description)
    print("****************************************************")
    print(result)
    print("****************************************************")
    return result

if __name__ == '__main__':
    # demo信息：数据输入口
    # topic = '黑胡椒烤鸡腿肉'
    # # description1='椰树牌椰汁是以海南盛产的椰子为原料，28年坚持在海南岛用新鲜椰子肉鲜榨，采用先进的加工技术及科学配方精制而成。它是一种不加香精、糖精、防腐剂不含胆固醇的天然植物蛋白饮料，其汁液均匀乳白、清醇，具有浓郁的天然椰香味，口感柔和、甜度适中、含有脂肪、蛋白质、十七种氨基酸和锌、铁、钙、锰等元素。于1991年被定为中国国宴饮料，产品畅销全国，远销世界33个国家和地区。'
    # description = '黑胡椒烤鸡腿肉,新手尝试,黑椒味,<15分钟,鸡边腿2个现磨胡椒碎适量洋葱1/4个苦菊1小把红椒1/4个 葱1棵姜3片蒜3瓣生抽2大勺老抽1小勺白糖30克白胡椒粉1克盐1克蜂蜜1勺橄榄油小勺苹果醋1勺 ,1.鸡边腿洗净去骨 2.用刀背轻剁鸡（目的可以使鸡肉松软、进味） 3.然后用竹签在表面和插一些小孔（这样可以防止鸡皮在烤的时候回缩） 4.葱切丝 5.蒜切大的碎粒、姜切片 6.葱、姜、蒜入碗加入生抽、老抽、白糖、白胡椒粉、盐拌匀 7.加入料酒拌匀 8.把鸡肉放入盘中均匀抹上腌料 9.转动现磨黑胡椒碎的瓶子，磨出粗粒 10.然后包裹保鲜膜入冰箱冷藏腌制一晚 11.制作前取出，捡出葱、姜、蒜不要 12.剩下的腌料里再加入蜂蜜拌匀成刷料 13.把鸡肉摆入烤架 14.入空气炸锅180度、烤25分钟左右 15.中途记得翻面和涮几次涮料 16.在烤肉期间，我们来制作一道简单的油醋沙拉来解解腻：苦菊洗净 17.洋葱切丝 18.红椒切丝 19.材料入碗，加入苹果醋 20.橄榄油 21.蜂蜜拌匀即可 22.烤好后取出，切块表面现磨出细粒胡椒碎，搭配沙拉即可食用 '
    # keywords=extract_keywords(description,topic)
    # ic(keywords)
    # exchanged_idioms=main_replace(keywords)
    # ic(exchanged_idioms)
    # ic(editdistance(exchanged_idioms,description))
    # result=Sbert_sort(exchanged_idioms,description)
    # ic(result)
    # sys.exit()

    sys.stdout = Logger('all2-使用新数据集随机采样+混合分数算法+随机生成120个-测试8+使用语义相似度模型+修复匹配不出成语的bug.log')
    # log.logger.debug('debug')
    # log.logger.info('info')
    # log.logger.warning('警告')
    # log.logger.error('报错')
    # log.logger.critical('严重')
    #加载数据集1
    # data=pd.read_csv('data/菜谱.csv')
    # topics=data['菜谱名称'].tolist()
    # descriptions=data['食材']+data['步骤']
    # descriptions=descriptions.tolist()
    #加载数据集2
    data=pd.read_csv('data/苏菜.csv')
    topics=data['名称'].tolist()
    descriptions=data['名称']+data['评价']
    descriptions=descriptions.tolist()

    #demo
    # topics=['蓝山咖啡']
    # descriptions=["咖咖咖咖咖咖咖咖咖咖蓝山咖啡，是指由产自牙买加蓝山的咖啡豆冲泡而成的咖啡。其中依档次又分为牙买加蓝山咖啡和牙买加高山咖啡。蓝山山脉位于牙买加岛（Jamaica） 东部，因该山在加勒比海的环绕下，每当天气晴朗的日子，太阳直射在蔚蓝的海面上，山峰上反射出海水璀璨的蓝色光芒，故而得名。蓝山最高峰海拔2256米，是加勒比地区的最高峰，也是著名的旅游胜地。这里地处地震带，拥有肥沃的火山土壤，空气清新，没有污染，气候湿润，终年多雾多雨，（平均降水为1980毫米，气温在27度左右）这样的气候造就了享誉世界的牙买加蓝山咖啡，同时也造就了世界上价格第二高的咖啡。此种咖啡拥有所有好咖啡的特点，不仅口味浓郁香醇，而且由于咖啡的甘、酸、苦三味搭配完美，所以完全不具苦味，仅有适度而完美的酸味。"]

    #加载模型
    pos_tagger = hanlp.load(hanlp.pretrained.mtl.OPEN_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)
    tokenizer = hanlp.load(hanlp.pretrained.tok.SIGHAN2005_PKU_BERT_BASE_ZH)
    sbertmodel = SentenceTransformer('stsb-roberta-base')
    # ic(topic,description)
    # print(len(topic),len(description))
    results={}
    #正常计算法
    # counter=0
    # for topic,description in tqdm(zip(topics,descriptions)):
    #     results[topic]=main(topic,description,pos_tagger,tokenizer,sbertmodel)
    #     counter+=1
    #     if counter>40:
    #         print("输出前40个examples\n")
    #         break
    #随机数采样测试
    L1=random_list(1,980,120)
    print(L1)
    for i in tqdm(L1):
        results[topics[i]]=main(topics[i],descriptions[i],pos_tagger,tokenizer,sbertmodel)
    # print(results)
    print("已输出随机采样的100条！\n")
    for k,v in results.items():
        print(k,v)
    # str=json.dumps(results)
    with open('result.txt','w',encoding='utf8') as f:
        f.write(str(results))





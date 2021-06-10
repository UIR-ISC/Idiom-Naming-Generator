#进行语义匹配尝试
from sentence_transformers import SentenceTransformer,util
from icecream import ic
import pandas as pd
import random


def Sbert_sort(model,exchanged_idioms,description):
    """
    返回一个pandas的dataframe
    exchanged_idioms:dataframe,包含修改之后的成语和解释
    """
    # model=SentenceTransformer('paraphrase-distilroberta-base-v1')
    #对所有的对应生成的成语语义进行编码
    idioms=exchanged_idioms['modified_idioms'].tolist()
    pinyin=exchanged_idioms['pinyin'].tolist()
    # explanation=exchanged_idioms['explanation'].tolist()

    #在explanation前加入成语本身
    explanation=exchanged_idioms['modified_idioms']+exchanged_idioms['explanation']
    explanation=explanation.tolist()
    # 使用成语解释进行embedding匹配
    embedding=model.encode(explanation)
    #直接使用变化后的成语embedding进行匹配
    # embedding=model.encode(idioms)
    # 对所有生成的成语直接进行编码处理
    # embedding=model.encode(modify_idioms)
    # 计算与描述相关的相似度
    cos_sim = util.pytorch_cos_sim(model.encode(description), embedding)
    ic(cos_sim)
    all_sentence_combinations=[]
    for i in range(len(cos_sim[0])):
        print(cos_sim[0][i])
        all_sentence_combinations.append([cos_sim[0][i],i])
    ic(all_sentence_combinations)
    all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)
    print("Top-10 most similar pairs:")
    result=[]
    score=[]
    for score, i in all_sentence_combinations[0:10]:
        # print(score, i)
        print("{} \t {} \t {:.4f}".format(idioms[i], explanation[i], cos_sim[0][i]))
        result.append(idioms[i])
        score.append(cos_sim[0][i])
    return result,score

if __name__ == '__main__':
    data=pd.read_csv('./data/苏菜.csv')
    name=data['名称'].tolist()
    description=data['评价'].tolist()
    # print(len(name),len(description))
    # print(random.sample(range(0,len(name)),1)[0])
    randnum=random.sample(range(0,len(name)),1)[0]
    sbertmodel = SentenceTransformer('stsb-roberta-base')
    print("Description:",description[randnum])
    embedding = sbertmodel.encode(description[randnum])
    print(embedding)
    print(embedding.size)
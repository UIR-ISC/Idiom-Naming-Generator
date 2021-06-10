import torch
from sentence_transformers import SentenceTransformer,util
from icecream import ic
import json


def mix_sort(bert_model,exchanged_idioms,description):

    """
    返回一个pandas的dataframe
    exchanged_idioms:dataframe,包含修改之后的成语和解释
    """
    #对所有的对应生成的成语语义进行编码
    origin_idioms=exchanged_idioms['origin_idioms'].tolist()
    idioms=exchanged_idioms['modified_idioms'].tolist()
    # pinyin=exchanged_idioms['pinyin'].tolist()
    # explanation=exchanged_idioms['explanation'].tolist()
    #在explanation前加入成语本身
    explanation=exchanged_idioms['modified_idioms']+exchanged_idioms['explanation']
    explanation=explanation.tolist()
    # 使用成语解释进行embedding匹配
    embedding=bert_model.encode(explanation)
    # print(embedding)
    #直接使用变化后的成语embedding进行匹配
    # embedding=model.encode(idioms)
    # 对所有生成的成语直接进行编码处理
    # embedding=model.encode(modify_idioms)
    # 计算与描述相关的相似度
    cos_sim = util.pytorch_cos_sim(bert_model.encode(description), embedding)
    ic(cos_sim)
    all_sentence_combinations=[]
    for i in range(len(cos_sim[0])):
        print(cos_sim[0][i])
        all_sentence_combinations.append([cos_sim[0][i],i])
    ic(all_sentence_combinations)
    #**************************************排序*******************************************#
    all_sentence_combinations = sorted(all_sentence_combinations, key=lambda x: x[0], reverse=True)
    print("Top-10 most similar pairs:")
    re_idioms=[]
    re_origin_idioms=[]
    re_explanation=[]
    bert_score=[]
    for score, i in all_sentence_combinations[0:10]:
        # print(score, i)
        # print("{} \t {} \t {:.4f}".format(idioms[i], explanation[i], cos_sim[0][i]))
        re_origin_idioms.append(origin_idioms[i])
        re_idioms.append(idioms[i])
        re_explanation.append(explanation[i])
        bert_score.append(cos_sim[0][i])
    #词频分数
    freq_score=[]
    with open('data/chengyu_freq.json') as f:
        freq_score_dict=json.load(f)#以词典的形式加载词频率
    for item in origin_idioms:
        freq_score.append(freq_score_dict[item])
    # print(freq_score)
    #混合分数  词频*SBert分数
    mixed_score=[i*j for i,j in zip(bert_score,freq_score)]
    result_turple=[(re_idioms[i],re_explanation[i],mixed_score[i]) for i in range(len(re_idioms))]
    result_turple=sorted(result_turple, key=lambda x: x[2], reverse=True)
    result=[]
    score=[]
    for i,e,s in result_turple[0:10]:
        # print(score, i)
        print("{} \t {} \t {:.4f}".format(i, e, s))
        result.append(i)
        score.append(s)

    return idioms,score


if __name__ == '__main__':
    with open('data/chengyu_freq.json') as f:
        freq_score=json.load(f)
    print(freq_score)
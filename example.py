#coding=utf8
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from main_func import main
import pandas as pd
import hanlp


if __name__ == '__main__':
    data = pd.read_csv('data/苏菜.csv')
    data=data[data['名称']=='油焖大虾']
    topics = data['名称'].tolist()[-2:]
    descriptions = data['名称'] + data['评价']
    descriptions = descriptions.tolist()[-2:]
    print(topics,descriptions)
    # 加载模型
    pos_tagger = hanlp.load(hanlp.pretrained.mtl.OPEN_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)
    tokenizer = hanlp.load(hanlp.pretrained.tok.SIGHAN2005_PKU_BERT_BASE_ZH)
    sbertmodel = SentenceTransformer('stsb-roberta-base')
    results = {}
    for i in tqdm(range(len(topics))):
        results[topics[i]]=main(topics[i],descriptions[i],pos_tagger,tokenizer,sbertmodel)
    print(results)
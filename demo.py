#coding=utf-8

from main_func import main
import hanlp
from sentence_transformers import SentenceTransformer
# main(topic,description,pos_tagger,tokenizer,model)

if __name__ == '__main__':
    demo_topic="香酥鲫鱼"
    demo_description="鲫鱼是饮食中常见的佳肴，营养价值高。常吃鲫鱼不仅能健身，还能减少肥胖，有助于降血压和降血脂的作用，一般人均可食用"
    pos_tagger = hanlp.load(hanlp.pretrained.mtl.OPEN_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)
    tokenizer = hanlp.load(hanlp.pretrained.tok.SIGHAN2005_PKU_BERT_BASE_ZH)
    sbertmodel = SentenceTransformer('stsb-roberta-base')
    main(demo_topic,demo_description,pos_tagger,tokenizer,sbertmodel)
#对成语每个字进行词性标注
import pandas as pd
import tqdm
import hanlp
import json
idioms=pd.read_csv('data/simplified_idioms_lazypinyin.csv')
idioms=idioms['idiom'].tolist()
print('成语库数量：',len(idioms))
cixing={}
pos_tagger = hanlp.load(hanlp.pretrained.mtl.OPEN_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)
for item in tqdm(idioms):
#     print(item,pos_tagger(item)['pos'],'||',pos_tagger([word for word in item])['pos'])
    cixing[item]=[pos_tagger(item)['pos'],pos_tagger([word for word in item])['pos']]
# cixing
#存储到json文件中
# with open('data/成语字词性.json','w') as f:
#     json.dump(cixing,f)
#构建统计学图表



#读取词性词典
with open('data/成语字词性.json','r') as f:
    cixing=json.load(f)

print(cixing)


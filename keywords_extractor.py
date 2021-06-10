import hanlp
import jieba.analyse
import pandas as pd


#获取停止词
def get_stopwords(file="data/cn_stopwords.txt"):
    stopwords=[]
    with open(file,'r',encoding='utf8') as f:
        for item in f.readlines():
            stopwords.append(item.strip())
    return stopwords
# stopwords=get_stopwords()

#获取关键词
def get_key_words(description,method='tf-idf'):
    #topK：提取的关键字数量，不指定则提取全部；
    # withWeight：设置为True指定输出词对应的IF-IDF权重
    if method=='textrank':
        #使用TextRank算法
        tags_pairs=jieba.analyse.textrank(description,topK=10,withWeight=True)#提取关键字标签
    else:
        #使用TF-IDF算法
        tags_pairs=jieba.analyse.extract_tags(description,topK=10,withWeight=True)#提取关键字标签
    tags_list=[]# 空列表用来存储拆分后的三个值
    for i in tags_pairs:# 打印标签、分组和TF-IDF权重
        tags_list.append((i[0],i[1]))#拆分三个字段
    tags_pd=pd.DataFrame(tags_list,columns=['word','weight'])#创建数据框
    return tags_pd
#测试
# keywords = get_key_words(description)
# print("#####################TF-IDF####################")
# print(keywords)
# # print(keywords['word'].tolist())
#
# keywords_tr = get_key_words(description, method='textrank')
# print("#####################textrank####################")
# print(keywords_tr)


#统计字频率，获取高频字
def count_word(string):
    string=removeStopwords(string)
    result={}
    for i in string:
        result[i]=string.count(i)
    result=sorted(result.items(), key=lambda item:item[1],reverse=True)
    result=[word[0] for word in result]
    return result

def removeStopwords(text):
#     punctuation = '。.!,;:?"\'、，；12345678
    stopwords=get_stopwords()
#     print(stopwords)
    for item in stopwords:
        if item in text:
            text=text.replace(item,'')
#             print(len(text))
#     text = re.sub(r'[{}]+'.format(stopwords),'',text)
    text=text.replace(" ",'')
#     print(text)
    return text.strip()

# print(count_word(description)[:20])


#加载hanlp的两个预训练的分词和词性标注器

# 抽取关键字的主函数（接口）
def extract_keywords(text,topic,pos_tagger):
    text=removeStopwords(text)
    #加载预训练模型
    # print("hanlp所有的预训练模型：\n")
    # print(hanlp.pretrained.ALL)
    # 多功能标签生成器
    # pos_tagger = hanlp.load(hanlp.pretrained.mtl.OPEN_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)
    # 加载中文分词预训练模型
    # tokenizer = hanlp.load(hanlp.pretrained.tok.SIGHAN2005_PKU_BERT_BASE_ZH)
    # 取TF-IDF和TextRank方法的交集
    keys = []
    keywords = get_key_words(text)['word'].tolist()
    textrank_keywords=get_key_words(text,method='textrank')['word'].tolist()
    print("only print textrank:",textrank_keywords)
    for i in range(len(keywords)):
        # print(keywords[i])
        if pos_tagger(keywords)['pos'][i][0] == 'NN':
            keys.append(keywords[i])
    wordcount = count_word(text)[:10]
    keys1 = []
    for word in wordcount:
        for ciyu in keys:
            if word in ciyu and word in topic:
                keys1.append(word)
                break

    #     keywords2=get_key_words(text,method='textrank')['word'].tolist()
    #     for item in keywords1:
    #         if item in keywords2:
    #             keys.append(item)
    return keys1[:2]

#测试
# 使用识别词性
# print(extract_keywords(description))
# pos_tagger('黑胡椒')

if __name__ == '__main__':
    pos_tagger = hanlp.load(hanlp.pretrained.mtl.OPEN_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_BASE_ZH)
    description="春天，在我们上海，家家户户都不会错过的一道菜，那就是腌笃鲜腌笃鲜的腌指咸肉，鲜指鲜肉和春笋，笃也就是小火慢炖意思。小时候家里哪怕生活再怎么拮据，到了这季节也会烧一锅过过瘾，解解馋，好像不吃这腌笃鲜错过了什么似的，做腌笃鲜就要大锅烧，食材足了才能烹饪出如此美味"
    topic="腌笃鲜"
    print(extract_keywords(description,topic,pos_tagger))
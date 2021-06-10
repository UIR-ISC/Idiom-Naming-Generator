import pandas as pd
from pypinyin import lazy_pinyin
from icecream import ic
# 将成语中对应读音的字进行替换
# 可以将列表拼音单独设置为一个列表，这样使用起来更好，因为pandas存储列表会有error
def main_replace(word):
    # 打开成语词典语料集
    idioms = pd.read_csv('data/simplified_idioms_lazypinyin.csv')
    # 将拼音上的音标删掉
    #     for i in range(len(idioms)):
    #         idioms.iloc[i,idioms.columns.get_loc('pinyin')]=lazy_pinyin(idioms['idiom'][i])
    # 检索含有word拼音的成语
    word_pinyins = lazy_pinyin(word) # 会返回一个列表

    filter_idioms = pd.DataFrame(columns=['idiom', 'explanation'])
    pinyin_demo = []
    for i in range(len(idioms)):
        data = idioms.loc[i]
        idiom_pinyin = lazy_pinyin(data['idiom'])
        if set(word_pinyins).issubset(set(idiom_pinyin)):
            pinyin_demo.append(idiom_pinyin)
            data = data.to_frame()
            data = data.T
            filter_idioms = pd.concat([filter_idioms, data])

    # 对检索出的结果进行替换
    idioms_demo = filter_idioms['idiom'].tolist()
    # print(idioms_demo)
    origin_demo=idioms_demo.copy()
    #     pinyin_demo=filter_idioms['pinyin'].tolist()
    explanation_demo = filter_idioms['explanation'].tolist()
    modify_idioms = []
    #     print("***********")
    # print(pinyin_demo)
    # print(word_pinyins)
    for i in range(len(idioms_demo)):
        # str1 = idioms_demo[i]
        # replace_index = pinyin_demo[i].index(word_pinyin)
        for word_pinyin,char in zip(word_pinyins,word):
            idioms_demo[i]= idioms_demo[i].replace(idioms_demo[i][pinyin_demo[i].index(word_pinyin)], char)
        modify_idioms.append(idioms_demo[i])
    if len(modify_idioms)==0 and len(word_pinyins)==2:#bug修复
        modify_idioms=main_replace(word[0])#权宜之计，后面的一般更关键
        return modify_idioms
    # print(origin_demo)
    print("初步替换之后的成语：", modify_idioms)
    modified_idioms = pd.DataFrame(
        {'origin_idioms':origin_demo,'modified_idioms': modify_idioms, 'pinyin': pinyin_demo, 'explanation': explanation_demo})
    return modified_idioms

#demo
#输入关键字列表
# ic(main_replace(['椒', '鸡']))
#
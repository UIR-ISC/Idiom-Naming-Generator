import json
import pandas as pd
import pickle
import jieba
from classifiers import *

def svm_classifier(text):
    f = open('svm_model/svm.model', 'rb')
    s = f.read()
    model = pickle.loads(s)
    predicted=[]
    # expected = '下落着落，去处。指不知道要寻找的人或物在什么地方。'
    for item in text:
        # print(model.classify(item),item)
        predicted.append(model.classify(item))
    return predicted

if __name__ == '__main__':
    idioms_file=pd.read_csv('data/simplified_idioms_lazypinyin.csv')
    # print(idioms)
    idioms=idioms_file['idiom'].tolist()
    explanation=idioms_file['explanation'].tolist()
    # print(explanation)
    explanations=[jieba.lcut(item) for item in explanation]
    # print(explanation)
    predicted=svm_classifier(explanations)
    print(predicted)

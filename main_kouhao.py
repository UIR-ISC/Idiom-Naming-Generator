import torch
import numpy as np
import math
import json

def softmax(inMatrix):
    """
    softmax计算公式函数
    :param inMatrix: 矩阵数据
    :return:
    """
    m,n = np.shape(inMatrix)  #得到m,n(行，列)
    outMatrix = np.mat(np.zeros((m,n)))  #mat生成数组
    soft_sum = 0
    for idx in range(0,n):
        outMatrix[0,idx] = math.exp(inMatrix[0,idx])  #求幂运算，取e为底的指数计算变成非负
        soft_sum +=outMatrix[0,idx]   #求和运算
    for idx in range(0,n):
        outMatrix[0,idx] = outMatrix[0,idx] /soft_sum #然后除以所有项之后进行归一化
    return outMatrix


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def standardization(data):
    mu = np.mean(data, axis=0)
    sigma = np.std(data, axis=0)
    return (data - mu) / sigma

# a = np.array([[1,2,1,2,1,1,3]])
# print(softmax(a))

with open('data/chengyu.txt', 'r', encoding='utf8') as f:
    list_word,word_freq=[],[]
    for item in f.readlines():
        list_word.append(item.split()[0])
        word_freq.append((item.split()[-1]))
# print(word_freq)
# print(list_word,word_freq)
# print(len(list_word),len(word_freq))
word_freq=[int(item) for item in word_freq]
# # print(type(word_freq[0]))
# a=np.array([word_freq])
# print(softmax(a))
# print(normalization(word_freq))
word_freq=normalization(word_freq)
freq={}
for word,fre in zip(list_word,word_freq):
    freq[word]=fre
print(freq)
with open('data/chengyu_freq.json','w',encoding='utf8') as f:
    f.write(json.dumps(freq))


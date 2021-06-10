import requests
import re
import winsound
import time
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
import sys

all_url=[]#存储网页地址
names=[]
ways=[]
specialities=[]
descriptions=[]
foods=[]
# Step_1 获取要爬取的所有网页的网址
def get_all_url(n):#使用此函数获取网页中菜的所有地址
    if(n==1):
        url="https://m.meishij.net/caixi/sucai1/"
    else:
        url='https://m.meishij.net/caixi/sucai1/p%s/'%n #%s相当于C语言中的%s，表示格式化一个对象为字符，同理%d表示格式化一个对象为整数
    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
    response=requests.get(url,headers=headers)#访问网页
    response.encoding="utf8"#设置接收编码格式
    patteren=re.compile(r'<a target="_blank" href="([a-zA-z]+://[^\s]*)">',re.S)
    # 正则表达式提取网页中的网址，re.S表示在整个文本中进行匹配，如果不加re.S，将只在一行进行匹配
    result=patteren.findall(response.text)#获取的王爷借过存储到result里
    all_url.append(result[0:10])#由于每页只有十道菜，result中只有前十条对应的是菜的网址，故我们只添加前十条
    return all_url
# Step_2 提取网页中的有用信息
def get_info(resp):
    name_pattern = re.compile(r'<h1>(.*)</h1>')# 正则表达式获取菜名信息
    food_pattern = re.compile(r'<span class="t">(.*)</span><span class="a">(.*)</span></a></div>')# 正则表达式获得主料信息
    fixing_pattern = re.compile(r'<div class="c_mtr_li"><span class="t1">(.*)</span><span class="a">(.*)</span></div>') # 正则表达式获得辅料信息
    fearture1_pattern = re.compile(r'<div class="cpargs cpargs2"><div class="i"></div>(.)</div>')# 正则表达式获得特征_1
    fearture2_pattern = re.compile(r'<div class="cpargs cpargs3"><div class="i"></div>(.*)</div>')# 正则表达式获得特征_2
    # pinjia_pattern=re.compile(r'<div class="cpdesw showOpenbtn" id="cpdesw"><p class="cpdes" id="cpdes">(.*)</p></div>')#提取评价

    name = name_pattern.findall(resp.text) # 提取菜名信息
    food = food_pattern.findall(resp.text)# 提取主料信息
    fixing = fixing_pattern.findall(resp.text)#提取辅料信息
    fearture1 = fearture1_pattern.findall(resp.text) #提取特征_1
    fearture2 = fearture2_pattern.findall(resp.text)#提取特征_2
    # pinjia=pinjia_pattern.findall(resp.text)#提取做菜的描述评价
    soup=BeautifulSoup(resp.text,'html.parser')
    if soup.find('p',attrs={'class':"cpdes",'id':"cpdes"})==None:
        pinjia='空'
    else:
        pinjia=soup.find('p',attrs={'class':"cpdes",'id':"cpdes"}).text
    # print(fearture1)
    # sys.exit()
    print(name)
    names.append(name[0])
    # output.write(name[0])#将菜名写入output文件，write函数不能写int类型的参数，所以使用str()转化
    # output.write('\t')#进入下一个单元格
    if len(fearture1)==0:
        ways.append('空')
    else:
        ways.append(fearture1[0])
    specialities.append(fearture2[0])
        # output.write(fearture1[0])#将特征_1写入output文件
    # output.write('\t')#进入下一个单元格
    # output.write(fearture2[0])#将特征_2写入output文件
    # output.write('\t')#进入下一个单元格
    # output.write(str(pinjia))  # 将评价写入output文件
    # output.write('\t')  # 进入下一个单元格
    descriptions.append(pinjia)
    #
    # for i in range(len(food)):
    #     for j in range(len(food[i])):
    #         output.write(str(food[i][j]))    #写入主料
    #         output.write('\t')
    # if(len(food)<11):
    #     output.write('\t'*2*(11-len(food))) #每道菜的主料数目不同，该行代码可使表格内容对齐
    #
    # for i in range(len(fixing)):
    #     for j in range(len(fixing[i])):
    #         output.write(str(fixing[i][j]))    #写入辅料
    #         output.write('\t')
    #
    # output.write('\n')    #换行

# Step_3 信息导出
def spider():
    # output = open('data/苏菜_2.csv','w',encoding='utf-8')#创建一个excel文件，编码格式为utf-8
    # output.write('名称\t做法\t特色\t主料\t评价')#写入标题栏
    # output.write('\t'*22)#使内容对齐
    # output.write('辅料\n')#写入标题栏
    # for i in [77,78,79,80]:
    for i in tqdm(range(len(all_url))):
         for j in range(len(all_url[i])):
            url2=all_url[i][j]
            response = requests.get(url2)#逐个访问网页，获得数据
            response.encoding = "utf-8" #设置接收编码格式
            # print(response.text=='')
            if response.text=='':
                continue
            get_info(response)#处理数据，提取信息
    saved_data=pd.DataFrame(data={'名称':names,'评价':descriptions,'做法':ways,'特色':specialities})
    saved_data.to_csv('data/苏菜.csv')
    # output.close()#关闭文件

# 主函数
if __name__ == '__main__':
    time_start=time.time()#记录程序开始的时间
    for i in tqdm(range(1,100)):#逐页获取菜谱的网页信息#改回100
        get_all_url(i)
    spider()#进行提取处理并导出
    duration=1000#提示音时长 1000ms=1s
    freq=440#提示音频率
    time_end=time.time()#记录程序结束时间
    print('totally cost',time_end-time_start)#打印程序运行的时间
    winsound.Beep(freq, duration * 10)  # 响铃提示程序结束
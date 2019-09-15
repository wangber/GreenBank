###从短文学网上爬取句子，随机取页，随机取页内句子###
# 在原来基础上进行改进 实现能够爬取多个类别的句子且能够进行类别指定 #
import requests
from bs4 import BeautifulSoup
import random

#定义构造url和类别值的函数
def get_type(order):
    types = ['【爱情语句】','【伤感语句】','【优美语句】','【想念的句子】']
    urls = {
        '【爱情语句】':'https://www.duanwenxue.com/yuju/aiqing/',
        '【伤感语句】':'https://www.duanwenxue.com/yuju/shanggan/',
        '【优美语句】':'https://www.duanwenxue.com/yuju/youmei/',
        '【想念的句子】':'https://www.duanwenxue.com/yuju/xiangnian/'
        }
    #根据得到的类别号从字典中挑出主url进行url的构造
    type = types[int(order)-1]
    base_url = urls[type]
    list_num = random.randint(1,100)
    url = base_url + "list_"+str(list_num)+".html"
    return type,url
    pass

#改写函数 接收url和类别 然后返回一个句子
def get_onesen(url,type):
    re=requests.get(url)
    soup = BeautifulSoup(re.text,"html.parser")
    sentence_set=soup.find_all("div",{"class":"list-short-article"})[0].text
    t=sentence_set.split(str(type))
    sentence_list=[]
    for t_instence in t:
        if len(t_instence.split("\n\n")[0])>=6:
            sentence_list.append(t_instence.split("\n\n")[0])
    j=random.randint(0,len(sentence_list))
    sen=sentence_list[j]
    return sen


#编写提供调用的api 提供类别返回句子
def juzi_api(order):
    type,url= get_type(order)
    sen = get_onesen(url,type)
    return sen



#for i in range(3):
#    print(juzi_api(2))
#for i in range(3):
#    print(get_onesen('https://www.duanwenxue.com/yuju/xiangnian/list_3.html','【想念的句子】'))

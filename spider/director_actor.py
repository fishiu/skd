# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import json
from time import time
from datetime import datetime

header_imdbcn = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Host': 'www.imdb.cn'
}


def extra_eng(s):
    m = 0
    for i in range(0, len(s)):
        if 'A' < s[i] < 'Z':
            m = i
            break
    return s[m:]


def find_rating(link):
    """
    获取评分
    @param link: 评分链接
    @return: 评分
    """
    url = link
    r2 = requests.get(url=url, headers=header_imdbcn).content.decode('utf-8')
    soup2 = bs(r2, "lxml")
    list6 = soup2.find_all(attrs={'class': 'Z_grade_rate'})
    return list6[0].text


def actor_info(link):
    """
    获取演员信息
    @param link: 演员链接
    @return: 演员信息
    """
    url = link
    r1 = requests.get(url=url, headers=header_imdbcn).content.decode('utf-8')
    soup1 = bs(r1, "lxml")
    list2 = soup1.find_all(attrs={'class': 'per_txt fr'})
    imdb_id = link[-10:-1]
    name = extra_eng(list2[0].h1.text)
    list3 = list2[0].find_all(attrs={'class': 'txt_bottom_r'})
    list4 = list2[0].find_all(attrs={'class': 'txt_bottom_l'})
    tag = []
    for i in list4:
        tag.append(i.text)
    if "性别：" in tag:
        sex = list3[tag.index("性别：")].text.strip()
    else:
        sex = ''
    if "地区：" in tag:
        nation = list3[tag.index("地区：")].text.strip()
    else:
        nation = ''
    if "出生：" in tag:
        age = list3[tag.index("出生：")].text.strip()
        age = 2020 - int(age[:4])
    else:
        age = ''

    # # 查找最有名的作品
    # list4 = soup1.find_all(attrs={'class': 'works_list'})
    # list5 = list4[0].find_all(attrs={'class': 'p1'})
    # s = 0
    # for i in list5:
    #     s = s + float(find_rating("https://www.imdb.cn" + i.a.attrs['href']))
    # avg_rat = s / len(list5)
    # return imdb_id, name, sex, nation, age, avg_rat
    list5 = soup1.find_all(attrs={'class': 'popularity'})
    rank=list5[0].span.text[3:]
    list6 = soup1.find_all(attrs={'class': 'edit_button'})
    idx = list6[0].a.attrs['data-id']
    url = "https://www.imdb.cn/index/person/film_json?id=" + idx + "&maker=4&type=1&sort=hot"
    r = requests.get(url=url, headers=header_imdbcn)
    j = json.loads(r.content.decode('utf-8'))
    ids = ['','','']
    m = 0
    for i in j:
        if int(i['year']) <= 2019 and int(i['year']) >= 2010 :
            ids[m]=i['url'][-10:-1]
            m = m + 1
        if m >= 3:
            break

    return imdb_id, name, sex, nation, age,rank, ids[0], ids[1], ids[2]


def dir_info(link):
    """
    获取导演信息
    @param link: 导演链接
    @return: 导演信息
    """
    url = link
    r1 = requests.get(url=url, headers=header_imdbcn).content.decode('utf-8')
    soup1 = bs(r1, "lxml")
    list2 = soup1.find_all(attrs={'class': 'per_txt fr'})
    imdb_id = link[-10:-1]
    name = extra_eng(list2[0].h1.text)
    list3 = list2[0].find_all(attrs={'class': 'txt_bottom_r'})
    list4 = list2[0].find_all(attrs={'class': 'txt_bottom_l'})
    tag = []
    for i in list4:
        tag.append(i.text)
    if "性别：" in tag:
        sex = list3[tag.index("性别：")].text.strip()
    else:
        sex = ''
    if "地区：" in tag:
        nation = list3[tag.index("地区：")].text.strip()
    else:
        nation = ''
    if "出生：" in tag:
        age = list3[tag.index("出生：")].text.strip()
        age = 2020 - int(age[:4])
    else:
        age = ''

    '''查找最有名的作品
    list4 = soup1.find_all(attrs={'class': 'works_list'})
    list5 = list4[0].find_all(attrs={'class': 'p1'})
    s = 0
    for i in list5:
        s = s + float(find_rating("https://www.imdb.cn" + i.a.attrs['href']))
    avg_rat = s / len(list5)'''
    list5 = soup1.find_all(attrs={'class': 'popularity'})
    rank = list5[0].span.text[3:]
    list6 = soup1.find_all(attrs={'class': 'edit_button'})
    idx = list6[0].a.attrs['data-id']
    url = "https://www.imdb.cn/index/person/film_json?id=" + idx + "&maker=1&type=1&sort=hot"
    r = requests.get(url=url, headers=header_imdbcn)
    j = json.loads(r.content.decode('utf-8'))
    ids = ['','','']
    m=0
    for i in j:
        if int(i['year']) <=2019 and int(i['year']) >= 2010 :
            ids[m]=i['url'][-10:-1]
            m=m+1
        if m>=3:
            break
    return imdb_id, name, sex, nation, age,rank, ids[0], ids[1], ids[2]


def find_a_d(imdb_id):
    """
    获取一部电影的导演、演员信息
    @param imdb_id: 电影imdb编号
    @return: 字典
    """
    url = 'https://www.imdb.cn/title/' + imdb_id + '/cast'
    r = requests.get(url=url, headers=header_imdbcn).content.decode('utf-8')
    # r.encoding = 'utf-8'
    # print(r)
    soup = bs(r, "lxml")
    list1 = soup.find_all(attrs={'class': 'item edit_item edit_item_wrap'})
    dic = {}
    for i in list1:
        key = i.h2.text
        div_list = i.find_all(attrs={'class': 'actors_l'})
        value = []
        j = 0
        for div in div_list:
            link = div.a.attrs['href']
            name = div.a.text.strip()
            value.append((link, name))
            j = j + 1
            if j >= 5:
                break
        # for div in div_list:
        #     link = div.a.attrs['href']
        #     name = div.a.text.strip()
        #     value.append((link, name))
        dic[key] = value
    actor_link = []
    dir_link = []
    for i in dic['演员']:
        b = 'https://www.imdb.cn' + i[0]
        actor_link.append((b, i[0][-10:-1]))

    for j in dic['导演']:
        c = 'https://www.imdb.cn' + j[0]
        dir_link.append((c, j[0][-10:-1]))

    dic1 = {}
    actor = []
    for link in actor_link:
        actor.append(actor_info(link[0]))
    director = []
    for link in dir_link:
        director.append(dir_info(link[0]))
    dic1['actor'] = actor
    dic1['director'] = director
    return dic1


if __name__ == '__main__':
    time_s = time()
    dic_res = find_a_d("tt0369610")
    print(json.dumps(dic_res, indent=2, sort_keys=True, ensure_ascii=False))
    print("[TIME] 共耗时%s" % datetime.fromtimestamp((time() - time_s)).strftime("%M分%S秒"))

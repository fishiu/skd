import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

ethnicity_dict = {}
orientation_dict = {}
all_actor = set()


def get_ethnicity():
    base_url = 'http://search.nndb.com/search/nndb.cgi?nndb=1&omenu=unspecified&query='
    df = pd.read_csv('./webdatamining/movie_omdb.csv', header=0)
    actors_in_mov = df['Actors']
    for x in actors_in_mov:
        actors = str(x).strip().split(',')
        for actor in actors:
            all_actor.add(actor)
            if actor in ethnicity_dict:
                continue
            url = base_url + '+'.join(actor.split())
            print(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            res = soup.find('p').get_text().strip()
            if (res[:5] == "Query"):  # 查询到了结果
                try:
                    print('result found')
                    line = soup.find_all('table')[3].find_all('tr')[1]
                    link = line.find_all('td')[0].font.a['href']
                    print(link)
                    response_ = requests.get(link)  # 个人页面
                    soup_ = BeautifulSoup(response_.text, 'html.parser')
                    block = soup_.find('table').find('table').find_all('table')[2].find('tr')
                    for p in block.find_all('p'):
                        if p.get_text()[:6] == "Gender":
                            try:  # 字段不一定存在
                                race = re.search(r'Race\sor\sEthnicity:[^:]*<br/>', str(p)).group()
                                race = race.split(':')[-1]
                                race = race.replace('</b>', '').replace('<br/>', '')
                                race = race.strip()
                                print(race)
                                ethnicity_dict[actor] = race
                            except:
                                ethnicity_dict[actor] = ''
                            try:
                                orientation = re.search(r'Sexual\sorientation:[^:]*<br/>', str(p)).group()
                                orientation = orientation.split(':')[-1]
                                orientation = orientation.replace('</b>', '').replace('<br/>', '')
                                orientation = orientation.strip()
                                print(orientation)
                                orientation_dict[actor] = orientation
                            except:
                                orientation_dict[actor] = ''
                except:  # 网页解析问题
                    ethnicity_dict[actor] = ''
                    orientation_dict[actor] = ''
            else:
                print('result not found')
                ethnicity_dict[actor] = ''
                orientation_dict[actor] = ''
    save()


def save():
    all_data = []
    for actor in all_actor:
        all_data.append([actor, ethnicity_dict[actor], orientation_dict[actor]])
    ed = pd.DataFrame(all_data, columns=['actorName', 'Ethnicity', 'Orientation'])
    ed.to_csv('./webdatamining/actor_ethnicity_and_orientation.csv')


get_ethnicity()

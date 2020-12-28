import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

import utils.config as config


def imdb_list(year, start_no):
    """
    获取某年电影，从start_no开始50部
    @param year: 年份
    @param start_no: 分页数据
    @return: (电影名称，电影ID)
    """
    url = "https://www.imdb.com/search/title/?title_type=feature&year=%d-01-01,%d-12-31&countries=us&sort=num_votes,desc&start=%d" % (
        year, year, start_no)
    print("[INFO] 爬取电影列表URL %s" % url)
    content = requests.get(url).content.decode('utf-8')
    soup = bs(content, "lxml")
    title_list = soup.find_all(attrs={'class': 'lister-item mode-advanced'})
    return [{"Title": title.h3.a.text, "ID": title.h3.a['href'][7:-1]} for title in title_list]


if __name__ == '__main__':
    start_year = 2010
    end_year = 2019
    res_list = []
    for y in range(start_year, end_year + 1):
        # for p in range(1, 51, 50):
        for p in range(1, 1001, 50):
            res_list.extend(imdb_list(y, p))
    df = pd.DataFrame(res_list)
    df.to_csv(config.path_movie_names, index=False, sep=',')

import requests
import bs4
import pandas as pd

import utils.config as config


def wiki_movie(min_year, max_year):
    """
    抓取wiki所有电影
    @param min_year: 开始年份
    @param max_year: 结束年份 + 1
    @return: 无返回，直接保存csv
    """
    movie_name_list = []
    year_list = []

    for i in range(int(min_year), int(max_year)):
        # url = "https://en.wikipedia.org/wiki/" + str(i) + "_in_film"
        url = "https://en.wikipedia.org/wiki/List_of_American_films_of_%d" % i
        print(url)
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.content, 'html.parser')

        for child in soup.findAll('a'):
            if '+' not in child.text:
                if child.parent.name == 'i':
                    if child.parent.parent.name == 'li':
                        movie_name_list.append(child.text)
                        year_list.append(str(i))

    df = pd.DataFrame({"Title": movie_name_list, "Year": year_list})
    df.to_csv(config.path_movie_names, index=False, sep=',')


if __name__ == '__main__':
    wiki_movie(2010, 2020)

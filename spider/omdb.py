import sys
import pandas as pd
import requests
import utils.config as config
import json
from time import time
from datetime import datetime


def title_omdb_query(title):
    """
    根据电影标题通过 omdb 查询电影信息
    @param title: 要查询的电影的标题
    @return: 返回电影信息字典
    """
    content = requests.get("http://www.omdbapi.com/?apikey=%s&t=%s" % (config.omdb_key, title)).content.decode("utf-8")
    return json.loads(content)


def id_omdb_query(imdb_id):
    """
    根据电影标题通过 omdb 查询电影信息
    @param imdb_id: 要查询的电影的id
    @return: 返回电影信息字典
    """
    try:
        content = requests.get("http://www.omdbapi.com/?apikey=%s&i=%s" % (config.omdb_key, imdb_id)).content.decode(
            "utf-8")
        return json.loads(content)
    except:
        raise Exception


def omdb_data_seg(start: int, end: int):
    """
    分段爬取omdb并保存
    @param start: 开始行号
    @param end: 结束行号
    @return:
    """
    # 读取
    movie_name_df = pd.read_csv(config.path_movie_names, header=0)
    movie_name_df_seg = movie_name_df[start - 1: end - 1]

    # 查询
    movie_data = []
    time_s = time()
    for i in range(start, end):
        movie_title, imdb_id = movie_name_df_seg.loc[i - 1, :]
        # print("[LOOP] 查询第%d条电影记录，电影名字是%s" % (i, movie_title))
        print("[LOOP] 查询第%d条电影记录，电影id是%s，电影名字是%s" % (i, imdb_id, movie_title))
        try:
            res = id_omdb_query(imdb_id)
            res["Idx"] = i
            movie_data.append(res)
        except:
            raise Exception("第%d条查询出错，电影id是%s，电影名字是%s" % (i, imdb_id, movie_title))

    # 保存
    try:
        movie_data_df = pd.read_csv(config.path_movie_omdb)
        movie_data_df = movie_data_df.append(movie_data)
        movie_data_df.to_csv(config.path_movie_omdb, index=False, sep=',')
    except Exception:
        raise Exception("保存出错")

    # 计算时间
    time_p = time() - time_s
    print("[TIME] 爬取第%d-%d条记录，耗时%s" % (start, end - 1, datetime.fromtimestamp(time_p).strftime("%M分%S秒")))
    print()


if __name__ == '__main__':
    step = 100
    task_s_time = time()
    for start_idx in range(8501, 9001, step):
        try:
            omdb_data_seg(start_idx, start_idx + step)
        except Exception as e:
            sys.stderr.write("[ERROR] %s\n" % e)
        except KeyboardInterrupt:
            sys.stderr.write("[ERROR]退出\n")
            break

    # 计算时间
    task_p_time = time() - task_s_time
    print("[DONE] 完成，耗时%s" % (datetime.fromtimestamp(task_p_time).strftime("%M分%S秒")))

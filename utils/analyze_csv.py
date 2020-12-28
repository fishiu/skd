import pandas as pd
import requests
import utils.config as config
import json
from time import time
from datetime import datetime

if __name__ == '__main__':
    movie_name_df = pd.read_csv(config.path_movie_omdb, header=0)
    print(movie_name_df.columns.values.tolist())

from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm
from os.path import exists
import requests
import pandas as pd
import numpy as np
import re
import codecs
import time
import json

# url = 'https://luatvietnam.vn/bang-gia-dat.html?YearRange=20202024&ProvinceId=32&DistrictId=510&StreetId=116036&LandTypeId=0&PriceFrom=100&PriceTo=100'
# html = requests.get(url).content
# df_list = pd.read_html(html)
# df = df_list[0]
# df.drop(0, axis=0, inplace=True)
# df = pd.DataFrame(df.iloc[:,4:8])
# df[4] = df[4].apply(lambda x: int(x.replace('.', '').replace('-', '0')))
# df[5] = df[5].apply(lambda x: int(x.replace('.', '').replace('-', '0')))
# df[6] = df[6].apply(lambda x: int(x.replace('.', '').replace('-', '0')))
# df[7] = df[7].apply(lambda x: int(x.replace('.', '').replace('-', '0')))
# print(np.mean(df[df!=0]))


# url = 'https://loibaihat.biz/lyric/7ocmd/hoakieu/'
# html = requests.get(url).content
# df_list = pd.read_html(html)

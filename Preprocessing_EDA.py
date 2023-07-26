
from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm
from os.path import exists
from fuzzywuzzy import fuzz
from unidecode import unidecode
from matplotlib import pyplot as plt
from utils import *
import requests
import numpy as np
import pandas as pd
import re
import codecs
import time
import json


# 1. Preprocessing:
"""
df = pd.read_csv('House-pricing-prediction/House-pricing-prediction/raw_housing_price.csv', index_col=0)
zip_obj = zip(list(df.columns), ['usable_area', 'land_area', 'bedroom', 'bathroom', 'legal',
                                       'date', 'id', 'address', 'price'])
dict_obj = dict(zip_obj)
df.rename(dict_obj, axis=1, inplace=True)
df['usable_area'] = df['usable_area'].apply(lambda x: float(str(x).split()[0].replace(',', '.')))
df['land_area'] = df['land_area'].apply(lambda x: float(str(x).split()[0].replace(',', '.')))
df['price'] = df['price'].apply(lambda x: convert_price(x))
df['address'] = df['address'].apply(lambda x: convert_address(x))

path = '/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-pricing-prediction/goverment_price.json'
with open(path) as json_file:
    json_list = json.load(json_file)

df['land_price'] = json_list
df = df.drop(['address', 'date', 'id'], axis=1)
df['legal'] = df['legal'].apply(lambda x:unidecode(x))
df['legal'] = df['legal'].apply(lambda x:x.replace(' ',''))
one_hot = pd.get_dummies(df['legal'], dtype=int)
df = df.join(one_hot)
df = df.drop('legal', axis=1)
print(df['land_area'][1],df['land_area'][1] == np.nan)

#Fill nan value:
for i in tqdm(range(df.shape[0])):
    if pd.isna(df['usable_area'][i]):
        df['usable_area'][i] = df['land_area'][i]
    if pd.isna(df['land_area'][i]):
        df['land_area'][i] = df['usable_area'][i]

df.to_csv('/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-pricing-prediction/housing_price.csv')
print(df)
"""
# 2. Data Inspection:
df = pd.read_csv(('/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-pricing-prediction/housing_price.csv'), index_col=0)
print(df)

# 3. Finding & Handling Missing Data:
# 4. Data Cleaning and Preprocessing:
# 5. Data Visualization:
# 6. Univariate Analysis:
# 7. Multivariate Analysis:
# 8. Feature Engineering:
# 9. Statistical Analysis:
# 10. Outlier Detection:

from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm
from os.path import exists
from fuzzywuzzy import fuzz
from unidecode import unidecode
import requests
import pandas as pd
import re
import codecs
import time
import json

def convert_price(string):
    if string!=None:
        if 'tỷ' in string:
            split = string.replace(' ', '').split('tỷ')
            b = float(split[0])
            if 'triệu' in string:
                m = float(split[1].replace('triệu', ''))
            else:
                m = 0
        else:
            b = 0
            m =  float(string.replace(' ', '').split('triệu')[0])
        return b*1000+m
    
def convert_address(string):
    # string = string.replace('Quận', '').replace('Huyện', '').replace('Phường', '').replace('Đường', '')
    string = string.replace('Tỉnh', '').replace(' Thành phố', '').replace('số', '').replace('(TP. Thủ Đức)','').replace('Quận','')
    string = string.replace('Thị xã','').replace(' Thành Phố', '').replace('TP','').replace('Huyện','')
    string = string.replace(' ', '').replace('.','').replace('(', '').replace(')','').replace('-','')
    string = unidecode(string)
    string = string.split(',')
    return string  
  
def get_street_value(data, princ, distr, ward, street):
    try:
        street_dict = data[princ]['districts'][distr]['streets']
        max_similar = 0
        street_addr = ''
        for str in street_dict.keys():
            similarity_ratio1 = fuzz.token_sort_ratio(street, str)
            similarity_ratio2 = fuzz.token_sort_ratio(street+ward, str)
            similarity_ratio = max(similarity_ratio1, similarity_ratio2)
            if similarity_ratio > max_similar:
                max_similar = similarity_ratio
                street_addr = str
        street_value = street_dict[street_addr]
        distr_value =  data[princ]['districts'][distr]['value']
        princ_value = data[princ]['value']
    except:
        street_value = '0'
        distr_value =  '0'
        princ_value = data[princ]['value']
    return [princ_value, distr_value, street_value]

def get_address_url(data, princ, distr, ward, street):
    [princ_value, distr_value, street_value] = get_street_value(data, princ, distr, ward, street)
    url = 'https://luatvietnam.vn/bang-gia-dat.html?YearRange=20202024&ProvinceId={}&DistrictId={}&StreetId={}'.format(princ_value, distr_value, street_value)
    return url
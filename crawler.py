from urllib.request import urlopen
from bs4 import BeautifulSoup
from tqdm import tqdm
from os.path import exists
import requests
import pandas as pd
import re
import codecs
import time

def update_dict(main_dict, src):
    """
    Update new info to dictionary
    main_dict: destination dictionary (ex: {'a': [1,2,3], 'b': [4,5,6], 'c':[7,8,9]}, 'e':[2,3,5])
    src: source dictionary (ex: {'a': 3, 'b': 0, 'c':6, 'e': 7})
    """
    if main_dict == {}:
        for key in src.keys():
            main_dict[key] = [src[key]]
    else:
        curr_num_examples = len(list(main_dict.values())[0])
        num_of_main_dict = len(main_dict)
        num_of_src_dict = len(src)
        if num_of_src_dict > num_of_main_dict:
            for key in src.keys():
                if key in main_dict:
                    main_dict[key].append(src[key])
                else:
                    main_dict[key] = [None] * curr_num_examples
                    main_dict[key].append(src[key])
        else:
            for key in main_dict.keys():
                if key in src:
                    main_dict[key].append(src[key])
                else:
                    main_dict[key].append(None)

def crawler(url, proxies={}):
    r = requests.get(url, proxies=proxies, timeout=20)
    # print(r.status_code)
    info_dict = {}
    bs = BeautifulSoup(r.text, 'html.parser')
    for main_info in bs.find_all('div', {'class':'info-attr clearfix'}):
        info_dict[main_info.find_all('span')[0].text] = main_info.find_all('span')[1].text
    info_dict['address'] = bs.find('div', {'class':'address'}).text
    info_dict['price'] = bs.find('div', {'class':'price'}).text
    return info_dict

def page_crawler(url, homes_dict={}, proxies={}):
    r = requests.get(url, proxies=proxies, timeout=20)
    bs = BeautifulSoup(r.text, 'html.parser')
    home_links = []
    for link in bs.find_all('a', {'class':'link-overlay'}):
        home_links.append(link.get('href'))
    for link in home_links:
        home_dict = crawler(link, proxies=proxies)
        update_dict(homes_dict, home_dict)
        next_page_link = bs.find('a', {'gtm-act':'next'}).get('href')
    return homes_dict, next_page_link

url = 'https://mogi.vn/mua-nha-dat?cp=75'


if exists('/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-prising-prediction/housing_price.csv'):
    df = pd.read_csv('/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-prising-prediction/housing_price.csv', index_col=0)
    homes_dict = df.to_dict('list')
    num_of_exam = df.shape[0]
else:
    homes_dict = {}
    num_of_exam = 0

crawled_data_size = 20000
proxies = {}
start_time = time.time()

while(True):
    try:
        with tqdm(total=crawled_data_size) as pbar:
            pbar.update(num_of_exam)
            while num_of_exam < crawled_data_size:
                privious_num = num_of_exam
                _,url = page_crawler(url=url, homes_dict=homes_dict, proxies=proxies)
                num_of_exam = len(list(homes_dict.values())[0])
                pbar.update(num_of_exam - privious_num)
        break
    except:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Elapsed time: {:.2f} seconds".format(elapsed_time))
        print('current url: ', url)
        homes_df = pd.DataFrame(homes_dict)
        homes_df.to_csv('/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-prising-prediction/housing_price1.csv')
        print("Connection refused by the server..")
        print("Let me sleep for 30 seconds")
        print("ZZzzzz...")
        print("ZPress Ctrl+C to stop program")
        time.sleep(30)
        print("Was a nice sleep, now let me continue...")
        continue



# df = pd.read_csv('D:\Workspaces\Projects\HousingPricePrediction\housing_price.csv')
# print(df)


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
from utils import *

# Scraping data of housing price in mogi.vn
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


if exists('/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-pricing-prediction/housing_price.csv'):
    df = pd.read_csv('/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-pricing-prediction/housing_price.csv', index_col=0)
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
        homes_df.to_csv('/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-pricing-prediction/housing_price1.csv')
        print("Connection refused by the server..")
        print("Let me sleep for 30 seconds")
        print("ZZzzzz...")
        print("ZPress Ctrl+C to stop program")
        time.sleep(30)
        print("Was a nice sleep, now let me continue...")
        continue

'''
Scraping data on government land prices by address from 
https://luatvietnam.vn/bang-gia-dat.html?YearRange=20202024
'''
# Get prince_name and these value:
url = 'https://luatvietnam.vn/bang-gia-dat.html?YearRange=20202024&ProvinceId=0&LandTypeId=0&PriceFrom=100&PriceTo=100'
r = requests.get(url, timeout=20)
bs = BeautifulSoup(r.text, 'html.parser')
selection = bs.find('select', {'class':"select select-form bg-ligh", 'name':"ProvinceId"})
Province = selection.find('option')
Province = str(Province).replace('option','').replace('<','').replace('>','').replace('/','').replace('value=','').replace(' ','').replace('.','').replace('-','').replace('TP','')
Province = unidecode(Province)
Province = Province.split('"')
Province = dict(zip(Province[2::2],Province[1::2]))
del Province["Tatca"]
# print(Province)

"""
#Get District_name and these value:
url = 'https://luatvietnam.vn/bang-gia-dat.html?YearRange=20202024&ProvinceId=26&DistrictId=0&LandTypeId=0&PriceFrom=100&PriceTo=100'
r = requests.get(url, timeout=20)
bs = BeautifulSoup(r.text, 'html.parser')
District = bs.find('select', {'name':"DistrictId"}).find('option')
District = str(District).replace('option','').replace('<','').replace('>','').replace('/','').replace('value=','').replace(' ','').split('"')
District = dict(zip(District[2::2],District[1::2]))

#Get Street_name and these value:

url = 'https://luatvietnam.vn/bang-gia-dat.html?YearRange=20202024&ProvinceId=25&DistrictId=118&StreetId=0&LandTypeId=0&PriceFrom=100&PriceTo=100'
r = requests.get(url, timeout=20)
bs = BeautifulSoup(r.text, 'html.parser')
Street = bs.find('select', {'name':"StreetId"}).find('option')
Street = str(Street).replace('option','').replace('<','').replace('>','').replace('/','').replace('value=','').replace(' ','').replace('.','').split('"')
Street = dict(zip(Street[2::2],Street[1::2]))
"""
addr_dict = {}
while(True):
    try:
        for i, princ in enumerate(tqdm(list(Province.keys()))):
            addr_dict[princ] = {}
            princ_value = Province[princ]
            pr_url = 'https://luatvietnam.vn/bang-gia-dat.html?YearRange=20202024&ProvinceId={}'.format(princ_value)
            while(True):
                try:
                    r = requests.get(pr_url, timeout=20)
                    break
                except:
                    print("Sleep 30s...")
                    print("ZPress Ctrl+C to stop program")
                    time.sleep(30)
                    print("continue...")
                    continue
            bs = BeautifulSoup(r.text, 'html.parser')
            District = bs.find('select', {'name':"DistrictId"}).find('option')
            District = str(District).replace('option','').replace('<','').replace('>','').replace('/','').replace('value=','')
            District = District.replace('Thị xã','').replace('Thành phố','').replace('Huyện','').replace('Quận','')
            District = unidecode(District)
            District = District.replace(' ','').replace('.','').replace('-','')
            District = District.split('"')
            District = dict(zip(District[2::2],District[1::2]))
            del District["Tatca"]
            Distr_dict = {}
            for j, distr in enumerate(tqdm(list(District.keys()))):
                Distr_dict[distr] = {}
                distr_value = District[distr]
                dist_url = pr_url + '&DistrictId={}'.format(distr_value)
                while(True):
                    try:
                        r = requests.get(dist_url, timeout=20)
                        break
                    except:
                        print("Sleep 30s...")
                        print("ZPress Ctrl+C to stop program")
                        time.sleep(30)
                        print("continue...")
                        continue
                bs = BeautifulSoup(r.text, 'html.parser')
                Street = bs.find('select', {'name':"StreetId"}).find('option')
                Street = str(Street).replace('option','').replace('<','').replace('>','').replace('/','').replace('value=','').replace(' ','').replace('.','')
                Street = unidecode(Street)
                Street = Street.split('"')
                Street = dict(zip(Street[2::2],Street[1::2]))
                del Street["Tatca"]
                Distr_dict[distr]['streets'] = Street
                Distr_dict[distr]['value'] = distr_value
            addr_dict[princ]['districts'] = Distr_dict
            addr_dict[princ]['value'] = princ_value
            file_path = "/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-pricing-prediction/address_value_data.json"
            with open(file_path, "w") as json_file:
                json.dump(addr_dict, json_file)
        break
    except:
        # Save the dictionary to a JSON file
        file_path = "/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-pricing-prediction/address_value_data.json"
        with open(file_path, "w") as json_file:
            json.dump(addr_dict, json_file)
        print("Sleep 30s...")
        print("ZPress Ctrl+C to stop program")
        time.sleep(30)
        print("continue...")
        continue


# Create a json file containing the average land price of the state corresponding to the addresses
path = '/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-pricing-prediction/address_value_data.json'
with open(path) as json_file:
    data = json.load(json_file)

goverment_price = []
for a in tqdm(list(df['address'])):
    princ = a[-1]
    distr = a[-2]
    ward = a[1]
    street = a[0]
    url = get_address_url(data, princ, distr, ward, street)
    while(True):
        try:
            html = requests.get(url).content
            df_list = pd.read_html(html)
            break
        except Exception as e:
            print("Error: ", e)
            file_path = "/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-pricing-prediction/goverment_price.json"
            with open(file_path, "w") as json_file:
                json.dump(goverment_price, json_file)
            print("Sleep 30s. Crtl+C to Stop program")
            time.sleep(30)
            print("Continue...")
            continue

    if len(df_list)>1:
        tb_df = df_list[0]
        tb_df.drop(0, axis=0, inplace=True)
        tb_df = pd.DataFrame(tb_df.iloc[:,4:8])
        tb_df[4] = tb_df[4].apply(lambda x: int(x.replace('.', '').replace('-', '0')))
        tb_df[5] = tb_df[5].apply(lambda x: int(x.replace('.', '').replace('-', '0')))
        tb_df[6] = tb_df[6].apply(lambda x: int(x.replace('.', '').replace('-', '0')))
        tb_df[7] = tb_df[7].apply(lambda x: int(x.replace('.', '').replace('-', '0')))
        goverment_price.append(np.mean(tb_df[tb_df!=0]))
    else:
        goverment_price.append(None)
file_path = "/home/namnguyen/Workspace/Projects/House-pricing-prediction/House-pricing-prediction/goverment_price.json"
with open(file_path, "w") as json_file:
    json.dump(goverment_price, json_file)

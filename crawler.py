from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


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

def crawler(url):
    html = urlopen(url)
    info_dict = {}
    bs = BeautifulSoup(html.read(), 'html.parser')
    for main_info in bs.find_all('div', {'class':'info-attr clearfix'}):
        info_dict[main_info.find_all('span')[0].text] = main_info.find_all('span')[1].text
    return info_dict

infos_dict = {}

url = 'https://mogi.vn/quan-binh-tan/mua-nha-hem-ngo/ban-nha-shr-1-tret-2-lau-4pn-san-do-xe-20m2-tai-lk-4-5-gia-2-3-ty-ctl-id22204971'
info_dict = crawler(url)
update_dict(infos_dict, info_dict)
print(infos_dict)

url = 'https://mogi.vn/quan-binh-tan/mua-nha-hem-ngo/ban-nha-shr-1-tret-2-lau-4pn-san-do-xe-20m2-tai-lk-4-5-gia-2-3-ty-ctl-id22204971'
info_dict = crawler(url)
update_dict(infos_dict, info_dict)
print(infos_dict)

url = 'https://mogi.vn/quan-binh-thanh/mua-nha-mat-tien-pho/can-tien-chua-benh-ban-gap-nha-vo-oanh-binh-thanh-60m2-1-ty-490-shr-id22121085'
info_dict = crawler(url)
update_dict(infos_dict, info_dict)
print(infos_dict)



import time
from lxml import etree
from config import Config
from tqdm import tqdm
from utils import *
import random


def get_equipment_list(config):
    """
    :param url_list:url列表
    :return:
    """
    url_equipment_list = []
    for url in tqdm(config.url_list, total=len(config.url_list)):
        url_equipment_list_part = []
        url_prefix = "https://en.wikipedia.org"
        page_text = get_page_text(url=url, webpage_data_path=config.webpage_data_path)
        tree = etree.HTML(page_text)
        if url == "https://en.wikipedia.org/wiki/List_of_main_battle_tanks_by_generation":
            li_list = tree.xpath('//*[@id="mw-content-text"]/div[@class="mw-parser-output"]/table[contains(@class,"wikitable")]/tbody/tr/td[1]')
        elif url == "https://en.wikipedia.org/wiki/List_of_main_battle_tanks_by_country":
            li_list = tree.xpath('//*[@id="mw-content-text"]/div[@class="mw-parser-output"]/table[contains(@class,"wikitable")]/tbody/tr/td[2]')
        else:
            li_list = tree.xpath('//*[@id="mw-content-text"]/div[@class="mw-parser-output"]//ul//li')
        for li in li_list:
            url_postfix_list = li.xpath("./a/@href")
            for url_postfix in url_postfix_list:
                if url_postfix.startswith("/wiki/List") or url_postfix.endswith(".php") or "action=edit" in url_postfix:
                    continue
                elif url_postfix.endswith(".htm") or url_postfix.endswith(".html") or url_postfix.endswith(".pdf"):
                    continue
                elif url_postfix.startswith("http") or url_postfix.startswith("#"):
                    continue
                else:
                    # 去除字符串中"#"
                    if "#" in url_postfix:
                        url_postfix = url_postfix[:url_postfix.index("#")]
                    url_equipment = url_prefix + url_postfix
                    url_equipment_list_part.append(url_equipment)
        url_equipment_list_part = list(dict.fromkeys(url_equipment_list_part))
        print(url, "分析完毕，包含", len(url_equipment_list_part), "条链接", end="，")
        origin_len = len(url_equipment_list)
        url_equipment_list.extend(url_equipment_list_part)
        url_equipment_list = list(dict.fromkeys(url_equipment_list))
        now_len = len(url_equipment_list)
        print("去重后实际贡献", now_len - origin_len, "条链接")
        time.sleep(config.waiting_time + random.random())
    # 去重
    url_equipment_list = list(dict.fromkeys(url_equipment_list))
    print("共有", len(url_equipment_list), "条链接")
    return url_equipment_list


if __name__ == '__main__':
    config = Config()
    url_list = config.url_list
    url_equipment_list_path = config.url_equipment_list_path
    url_equipment_list = get_equipment_list(config)
    print(len(url_equipment_list))



import os
import json
import requests


def list2sentence(phrase_list):
    """
    将字符串数组列表拼接成句子
    """
    sentence = ''
    for word in phrase_list:
        sentence += word
    return sentence


def get_page_text(url, webpage_data_path):
    """
    根据url返回页面内容
    """
    page_text = None
    # 从本地文件读取数据
    if os.path.exists(webpage_data_path):
        with open(webpage_data_path, 'r', encoding='utf8') as fp:
            webpage_list = json.load(fp)
        for webpage in webpage_list:
            if webpage["wiki_url"] == url:
                page_text = webpage["page_text"]
                print("本地文件读取:", url)
                break
    else:
        webpage_list = []

    # 从网页爬取数据
    if page_text is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35'
        }
        page_text = requests.get(url=url, headers=headers).text
        print("网页爬取数据:", url)
        # 保存数据
        webpage = dict()
        webpage["wiki_url"] = url
        webpage["page_text"] = page_text
        webpage_list.append(webpage)
        with open(webpage_data_path, 'w') as f:
            json.dump(webpage_list, f)

    return page_text

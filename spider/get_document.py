import os
from lxml import etree
from utils import *
from config import Config
from tqdm import tqdm
import time

if __name__ == '__main__':
    config = Config()
    # 获取需要爬取的url
    url_list = []
    with open(config.bingSearch_result_path, 'r', encoding='utf8') as fp:
        bingSearch_list = json.load(fp)
    for bingSearch_result in bingSearch_list:
        url_list.extend(bingSearch_result["url_list"])
    print("去重前url长度：", len(url_list))
    url_list = list(dict.fromkeys(url_list))
    print("需要爬取的url长度：", len(url_list))

    # 去除已经爬取的url
    if os.path.exists(config.raw_sentence_path):
        with open(config.raw_sentence_path, 'r', encoding='utf8') as fp:
            document_list = json.load(fp)
    else:
        document_list = []
    print("已经爬取的url长度：", len(document_list))
    remove_list = []
    new_url_list = []
    for url in url_list:
        add_flag = True
        for document in document_list:
            if url == document["url"]:
                add_flag = False
        if add_flag:
            new_url_list.append(url)
    url_list = new_url_list
    print("实际需要爬取的url长度：", len(url_list))

    # 开始爬取
    for url in tqdm(url_list, total=len(url_list)):
        if not url.startswith("http"):
            url = "http://" + url
        document = dict()
        document["url"] = url
        try:
            page_text = get_page_text(url=url, webpage_data_path=config.webpage_sentence_path)
            tree = etree.HTML(page_text)
            sentence_list = tree.xpath('//text()')
            this_document = ''
            for sentence in sentence_list:
                this_document += sentence
            document["document"] = this_document
            document_list.append(document)
            if len(document_list) % 5 == 0:
                with open(config.raw_sentence_path, 'w') as f:
                    json.dump(document_list, f)
                print("已爬取", len(document_list), "个文档")
        except Exception as e:
            print(e)
            print(url, "爬取失败")
            time.sleep(5)
        time.sleep(0)

    # 写入json文件
    with open(config.raw_sentence_path, 'w') as f:
        json.dump(document_list, f)
    print("完成！！！共采集到", len(document_list), "个文档")

from lxml import etree
from utils import *
from config import Config
from py2neo import *
from tqdm import tqdm
import time

if __name__ == '__main__':
    config = Config()
    # 连接neo4j 数据库，获取实体名称
    graph = Graph('bolt://localhost:7687', auth=('neo4j', '123456'))
    node_matcher = NodeMatcher(graph)
    equipment_nodes = node_matcher.match("equipment")
    print("共有", len(equipment_nodes), "个装备需要爬取")

    # 去除已经爬取过的实体
    if os.path.exists(config.url_sentence_list_path):
        with open(config.url_sentence_list_path, 'r', encoding='utf8') as fp:
            url_sentence_list = json.load(fp)
    else:
        url_sentence_list = []
    equipment_name_list = []
    print("已爬取", len(url_sentence_list), "个装备实体")

    for equipment_node in equipment_nodes:
        equipment_name = equipment_node["name"]
        add_flag = True
        for url_sentence in url_sentence_list:
            if equipment_name == url_sentence["name"]:
                add_flag = False
                break
        if add_flag:
            equipment_name_list.append(equipment_name)
    print("需要爬取", len(equipment_name_list), "个装备实体")

    # 开始爬取
    for equipment_name in tqdm(equipment_name_list, total=len(equipment_name_list)):
        equipment = dict()
        equipment["name"] = equipment_name
        url = "https://www.google.com/search?q=" + equipment["name"] + "&sxsrf=ALiCzsa6rqoTiz6mrmFBxm6Pe_OD4haCng%3A1669786854655&source=hp&ei=5uyGY7fBJeez0PEPjdaTyAI&iflsig=AJiK0e8AAAAAY4b69nhjARhy3lkoUkroGXjsP9ZLH7GX&ved=0ahUKEwi3zMfimNX7AhXnGTQIHQ3rBCkQ4dUDCAo&uact=5&oq=10TP&gs_lcp=Cgdnd3Mtd2l6EAMyBAgjECcyCggAEIAEEIcCEBQyBQgAEIAEMgUIABCABDINCAAQgAQQsQMQgwEQCjIFCAAQgAQyBwgAEIAEEAoyBwgAEIAEEAoyBwgAEIAEEAoyBwgAEIAEEAo6BQgAEJECOgUILhCRAjoICAAQgAQQsQM6CAguEIMBELEDOgsIABCABBCxAxCDAToICC4QsQMQgwE6CwguEIAEEMcBEK8BOgsILhCABBCxAxDUAjoICAAQsQMQgwE6CAguEIAEEOUEUABY5BFgmxZoAXAAeACAAcoCiAHhC5IBBTItMy4ymAEAoAEB&sclient=gws-wiz"
        # url = "https://www.google.com/search?q=10TP"
        page_text = get_page_text(url=url, webpage_data_path=config.webpage_sentence_path)
        tree = etree.HTML(page_text)
        url_list = tree.xpath('//div[@class="yuRUbf"]/a/@href')
        equipment["url_list"] = url_list
        assert len(url_list) > 0
        url_sentence_list.append(equipment)
        print(equipment["name"], ":", len(url_list))
        time.sleep(10)

    # 写入json文件
    with open(config.url_sentence_list_path, 'w') as f:
        json.dump(url_sentence_list, f)
    print("完成！！！共采集到", len(url_sentence_list), "个链接")

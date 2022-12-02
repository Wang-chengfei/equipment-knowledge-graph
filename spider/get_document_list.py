from lxml import etree
from utils import *
from config import Config
from py2neo import *
from tqdm import tqdm
import time

if __name__ == '__main__':
    config = Config()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35'
    }
    # 连接neo4j 数据库，获取实体名称
    graph = Graph('bolt://localhost:7687', auth=('neo4j', '123456'))
    node_matcher = NodeMatcher(graph)
    equipment_nodes = node_matcher.match("equipment")
    print("共有", len(equipment_nodes), "个装备需要爬取")

    # 获取已经爬取的实体
    if os.path.exists(config.bingSearch_result_path):
        with open(config.bingSearch_result_path, 'r', encoding='utf8') as fp:
            bingSearch_list = json.load(fp)
    else:
        bingSearch_list = []
    equipment_name_list = []
    print("已爬取", len(bingSearch_list), "个装备实体")

    # 去除已经爬取过的实体
    for equipment_node in equipment_nodes:
        equipment_name = equipment_node["name"]
        add_flag = True
        for bingSearch_result in bingSearch_list:
            if equipment_name == bingSearch_result["name"]:
                if bingSearch_result["url_list"] is not None and len(bingSearch_result["url_list"]) > 0:
                    add_flag = False
        if add_flag:
            equipment_name_list.append(equipment_name)
    print("需要爬取", len(equipment_name_list), "个装备实体")

    # 开始爬取
    for equipment_name in tqdm(equipment_name_list, total=len(equipment_name_list)):
        remove_idx = []
        for idx, bingSearch_result in enumerate(bingSearch_list):
            if equipment_name == bingSearch_result["name"]:
                remove_idx.append(idx)
        for idx in remove_idx:
            bingSearch_list.pop(idx)
        equipment = dict()
        equipment["name"] = equipment_name
        equipment["url_list"] = []
        # url = "https://www.bing.com/search?q=10TP"
        search_url = "https://www.bing.com/search?q=" + equipment["name"]
        try:
            page_text = get_page_text(url=search_url, webpage_data_path=config.webpage_bingSearch_path)
            # print(page_text)
            tree = etree.HTML(page_text)
            url_list = tree.xpath('//ol[@id="b_results"]/li//div[@class="b_attribution"]/cite/text()')
            for url in url_list:
                if "..." in url:
                    new_url = tree.xpath('//cite[contains(text(),"' + url + '")]/../../preceding-sibling::*[1]//a/@href')
                    if len(new_url) == 0:
                        new_url = tree.xpath('//cite[contains(text(),"' + url + '")]/../preceding-sibling::*[1]//a/@href')
                    url = new_url
                if isinstance(url, str):
                    equipment["url_list"].append(url)
                elif len(url) > 0:
                    equipment["url_list"].append(url[0])
            for url in equipment["url_list"]:
                print(url)
            assert len(equipment["url_list"]) > 0
            bingSearch_list.append(equipment)
            print(equipment["name"], ":", len(equipment["url_list"]))
            if len(bingSearch_list) % 10 == 0:
                # 写入json文件
                with open(config.bingSearch_result_path, 'w') as f:
                    json.dump(bingSearch_list, f)
                print("数据已保存，已爬取", len(bingSearch_list), "个实体")
        except Exception as e:
            print(e)
            print("爬取", search_url, "出现异常，稍后继续爬取...")
            time.sleep(5)
        time.sleep(0)

    # 写入json文件
    with open(config.bingSearch_result_path, 'w') as f:
        json.dump(bingSearch_list, f)
    print("完成！！！共采集到", len(bingSearch_list), "个实体")

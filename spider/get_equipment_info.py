from lxml import etree
from config import Config
from utils import *
import re
import unicodedata


def get_equipment_info(url, config):
    """
    :param url:维基百科装备 url
    :return:装备字典
    """
    page_text = get_page_text(url=url, webpage_data_path=config.webpage_data_path)
    tree = etree.HTML(page_text)
    # 装备字典
    equipment = dict()
    # 提取装备名称
    name = tree.xpath('//*[@id="firstHeading"]//text()')
    if len(name) == 0:
        print("提取装备名称出错 " + url)
        return
    name = name[0]
    equipment["name"] = name
    equipment["wiki_url"] = url
    # 提取描述性文本
    equipment["text_info"] = dict()
    # 提取描述性文本——所有
    document = tree.xpath('//*[@id="mw-content-text"]/div[@class="mw-parser-output"]//p//text()')
    equipment["text_info"]["document"] = list2sentence(document).strip()
    # # 提取描述性文本——简述
    # h2_label_list = tree.xpath('//*[@id="mw-content-text"]/div[@class="mw-parser-output"]/h2')
    # if len(h2_label_list) == 0:
    #     description = tree.xpath('//*[@id="mw-content-text"]/div[@class="mw-parser-output"]/p//text()')
    #     equipment["text_info"]["description"] = list2sentence(description).strip()
    # else:
    #     description = h2_label_list[0].xpath('./preceding-sibling::p//text()')
    #     equipment["text_info"]["description"] = list2sentence(description).strip()
    # # 提取描述性文本——分类
    # title_list = []
    # content_list = []
    # for h2_label in h2_label_list:
    #     title = h2_label.xpath('./*[@class="mw-headline"]/text()')[0]
    #     content = h2_label.xpath('./following-sibling::p//text()')
    #     title_list.append(title)
    #     content_list.append(content)
    # for i in range(len(content_list) - 1):
    #     length = len(content_list[i]) - len(content_list[i + 1])
    #     content_list[i] = content_list[i][:length]
    #     equipment["text_info"][title_list[i]] = list2sentence(content_list[i]).strip()
    # if len(title_list) > 0:
    #     equipment["text_info"][title_list[len(title_list) - 1]] = list2sentence(content_list[len(title_list) - 1]).strip()

    # 提取表格信息
    equipment["table_info"] = dict()

    # 将表格划分成两部分
    equipment["table_info"]["Totality"] = dict()
    equipment["table_info"]["Specification"] = dict()
    is_specification = False
    tr_list = tree.xpath('//*[@id="mw-content-text"]/div[@class="mw-parser-output"]//table[contains(@class,"infobox")][1]/tbody/tr')
    for tr in tr_list:
        titles = tr.xpath('./th//text()')
        contents = tr.xpath('./td//text()')
        if len(titles) > 0 and titles[0].startswith("Specifications"):
            is_specification = True
        if len(titles) > 0 and len(contents) > 0:
            title = ''
            content = ''
            for i in titles:
                if '.' not in i:
                    title = title + i + ' '
            title = unicodedata.normalize(config.normalize_signature, title)
            title = re.sub(r" +", " ", title)
            title = title.strip()

            # 丢弃Variants与References
            if title in ["Variants", "References"]:
                continue

            # 特殊处理 "See" "Varies" "View"
            if contents[0].lower().startswith("see") or \
                    contents[0].lower().startswith("varies") or \
                    contents[0].lower().startswith("view") or \
                    contents[0].lower().startswith("users"):
                if is_specification:
                    continue
                else:
                    if len(tr.xpath('./td//a/@href')) > 0:
                        span_id = tr.xpath('./td//a/@href')[0].split("#")[-1]
                    else:
                        continue
                    search_list = []
                    # 获取两个h2标签之间的所有标签
                    h2_label_h2 = tree.xpath('//span[@id="' + span_id + '"]/../following-sibling::*[position() < (count(//span[@id="' + span_id + '"]/../following-sibling::*) - count(//span[@id="' + span_id + '"]/../following-sibling::h2[1]/following-sibling::*))]')
                    for label in h2_label_h2:
                        if label.tag == "ul":
                            this_list = label.xpath('.//li/a[1]/text()')
                        else:
                            this_list = label.xpath('.//ul/li/a[1]/text()')
                        search_list.extend(this_list)

                    content = search_list

            # 特殊处理可能为列表的数据，包括Wars, Place of origin, Used by, Type, Manufacturer, Designer
            elif title in ["Place of origin", "Used by", "Wars", "Type", "Manufacturer", "Designer"]:
                content = contents

            # 一般情况处理
            else:
                for i in contents:
                    content = content + i + ' '
                content = content.strip()

            if is_specification:
                equipment["table_info"]["Specification"][title] = content
            else:
                equipment["table_info"]["Totality"][title] = content

            # 特殊处理armament
            if "armament" in title.lower():
                armament_list = tr.xpath('./td//a/@href')
                content = []
                for armament in armament_list:
                    if armament.startswith("/wiki/"):
                        armament = armament[6:].replace("_", " ")
                        content.append(armament)
                title = "Armament"
                if title not in equipment["table_info"]["Totality"].keys():
                    equipment["table_info"]["Totality"][title] = []
                equipment["table_info"]["Totality"][title].extend(content)

    # 返回字典
    return equipment


if __name__ == '__main__':
    config = Config()
    # url = config.example_url
    url = "https://en.wikipedia.org/wiki/Assault_gun"
    equipment = get_equipment_info(url=url, config=config)
    # 写入json文件
    with open(config.raw_data_example_path, 'w') as f:
        json.dump(equipment, f)
    print(equipment)
    print("数据已写入至：", config.raw_data_example_path)


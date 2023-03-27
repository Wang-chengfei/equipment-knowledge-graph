import json
import unicodedata
from config import Config

if __name__ == '__main__':
    config = Config()
    with open(config.relation2id_path, 'r', encoding='utf8') as fp:
        relation2id = json.load(fp)
    relation_list = []
    for relation in relation2id:
        if relation == "None":
            continue
        relation_type = relation.split("/")[3]
        relation_list.append(relation_type)
    with open(config.raw_data_path, 'r', encoding='utf8') as fp:
        equipment_list = json.load(fp)

    print("装备列表长度：", len(equipment_list))
    entity_list = []
    attribute_type_count = dict()
    relation_type_count = dict()
    filtered_relation_type_count = dict()
    attribute_type = dict()
    relation_type = dict()
    for equipment in equipment_list:
        # 根据Specifications关键字筛选
        relation_flag = False
        for key in equipment["table_info"]["Totality"].keys():
            if key in relation_list:
                relation_flag = True
        if len(equipment["table_info"]["Specification"]) == 0 or not relation_flag:
            print("筛选掉的实体：", equipment["name"], equipment["wiki_url"])
            continue
        # print("未被筛选的实体：", equipment["name"], equipment["wiki_url"])
        entity_list.append(equipment["name"])
        # 属性
        for key, value in equipment["table_info"]["Specification"].items():
            key = unicodedata.normalize(config.normalize_signature, key)
            attribute_type_count[key] = attribute_type_count.get(key, 0) + 1
        # 关系
        for key, value in equipment["table_info"]["Totality"].items():
            key = unicodedata.normalize(config.normalize_signature, key)
            relation_type_count[key] = relation_type_count.get(key, 0) + 1
    # 将部分关系集合移动至属性集合
    for key, value in relation_type_count.items():
        if key not in relation_list:
            attribute_type_count[key] = relation_type_count[key]
        else:
            filtered_relation_type_count[key] = relation_type_count[key]
    relation_type_count = filtered_relation_type_count
    # 排序
    attribute_type_count = dict(sorted(attribute_type_count.items(), key=lambda i: i[-1], reverse=True))
    relation_type_count = dict(sorted(relation_type_count.items(), key=lambda i: i[-1], reverse=True))
    # 将关系类别映射为id
    for key, value in attribute_type_count.items():
        attribute_type[key] = len(attribute_type)
    for key, value in relation_type_count.items():
        relation_type[key] = len(relation_type)
    # 打印实体列表，属性集合，关系集合
    print("\n实体列表：-------------------------------------")
    print(len(entity_list))
    print(entity_list)
    print("属性集合：-------------------------------------")
    print(len(attribute_type_count))
    print(attribute_type_count)
    print(attribute_type)
    print("关系集合：-------------------------------------")
    print(len(relation_type_count))
    print(relation_type_count)
    print(relation_type)

import json
import unicodedata
import re
from config import Config


if __name__ == '__main__':
    config = Config()
    with open(config.raw_data_path, 'r', encoding='utf8') as fp:
        equipment_list = json.load(fp)
    with open(config.relation2id_path, 'r', encoding='utf8') as fp:
        relation2id = json.load(fp)
    relation_list = []
    for relation in relation2id:
        if relation == "None":
            continue
        relation_type = relation.split("/")[3]
        relation_list.append(relation_type)
    processed_equipment_list = []

    # 开始处理
    discard_list = ["", ",", "/", "[", "]", "citation needed", "and", "now", "at", "&", "later",
                    "then", "of", "hybrid", "–", "see",  "{", "}", "none", ":", "in", "x", ";",
                    "!", "(", ")", "view", "part of", "from", "avre", "list", "project", "short",
                    "long-range", "large", "medium", "big", "users", "army"]
    content_num = 0
    name_num = 0
    repetition_num = 0
    for equipment in equipment_list:
        # 筛选掉不符合要求和重复的实体
        # 重复筛选
        repetition_flag = False
        for entity in processed_equipment_list:
            if entity["name"] == equipment["name"]:
                repetition_flag = True
        if repetition_flag:
            repetition_num += 1
            print("重复筛选:", equipment["name"], equipment["wiki_url"])
            continue
        # 内容筛选
        relation_count = 0
        for key in equipment["table_info"]["Totality"].keys():
            if key in relation_list:
                relation_count += 1
        if len(equipment["table_info"]["Specification"]) == 0 or relation_count < 2:
            content_num += 1
            print("内容筛选:", equipment["name"], equipment["wiki_url"])
            continue
        # 名称筛选
        if re.search(r"[^A-Za-z0-9 -]", equipment["name"]) is not None:
            name_num += 1
            print("名称筛选:", equipment["name"], equipment["wiki_url"])
            continue

        # print("未被筛选的实体：", equipment["name"], equipment["wiki_url"])
        processed_equipment = dict()
        equipment_name = equipment["name"]
        equipment_name = re.sub(r"\(.*?\)", "", equipment_name)
        equipment_name = re.sub(r" +", " ", equipment_name)
        equipment_name = equipment_name.strip()
        processed_equipment["name"] = equipment_name
        processed_equipment["origin_name"] = equipment["name"]
        processed_equipment["relation"] = dict()
        processed_equipment["attribute"] = dict()
        equipment_items = dict(equipment["table_info"]["Specification"], **equipment["table_info"]["Totality"])
        for key, value in equipment_items.items():
            key = unicodedata.normalize(config.normalize_signature, key)
            key = re.sub(r" +", " ", key)
            key = key.strip()
            # 处理字符串数据（属性）
            if isinstance(value, str):
                value = unicodedata.normalize(config.normalize_signature, value)
                value = re.sub(r"\[.*?\]", "", value)
                # value = re.sub(r"\(.*?\)", "", value)
                value = re.sub(r" +", " ", value)
                value = value.strip()
            # 处理列表数据（关系）
            elif isinstance(value, list):
                # 特殊处理Type
                if key == "Type":
                    content = ''
                    for war in value:
                        if not war.startswith("."):
                            content += war + " "
                    content = unicodedata.normalize(config.normalize_signature, content)
                    content = re.sub(r"\[.*?\]", "", content)
                    content = re.sub(r"\(.*?\)", "", content)
                    content = re.sub(r"[^A-Za-z ,\n/-]", "", content)
                    content = re.sub(r"-cwt", "", content)
                    content = re.sub(r"-ton", "", content)
                    content = re.sub(r"ton", "", content)
                    content = re.sub(r"cwt", "", content)
                    content = re.sub(r" +", " ", content)
                    content = re.sub(r"truck truck", "truck", content)
                    content = content.strip()
                    if content.startswith("x "):
                        content = content[2:]
                    if content.endswith(" x"):
                        content = content[:len(content) - 2]
                    if content.startswith("and "):
                        content = content[4:]
                    if content.endswith(" and"):
                        content = content[:len(content) - 4]
                    content = re.sub(r" +", " ", content)
                    content = content.strip().lower()
                    value = []
                    if "/" in content:
                        for item in content.split("/"):
                            item = item.strip()
                            if item is not None and item.lower() not in discard_list:
                                value.append(item)
                    elif "," in content:
                        for item in content.split(","):
                            item = item.strip()
                            if item is not None and item.lower() not in discard_list:
                                value.append(item)
                    elif "\n" in content:
                        for item in content.split("\n"):
                            item = item.strip()
                            if item is not None and item.lower() not in discard_list:
                                value.append(item)
                    else:
                        value = content
                # 处理除了Types之外的其它关系
                else:
                    content = []
                    for war in value:
                        war = unicodedata.normalize(config.normalize_signature, war)
                        war = re.sub(r"\[.*?\]", "", war)
                        war = re.sub(r"\[", "", war)
                        war = re.sub(r"\]", "", war)
                        war = re.sub(r"\(.*?\)", "", war)
                        war = re.sub(r"\(", "", war)
                        war = re.sub(r"\)", "", war)
                        war = re.sub(r"and others", "", war)
                        war = war.strip()
                        war = war.strip(".")
                        if war.startswith("x "):
                            war = war[2:]
                        if war.endswith(" x"):
                            war = war[:len(war) - 2]
                        if war.startswith("and "):
                            war = war[4:]
                        if war.endswith(" and"):
                            war = war[:len(war) - 4]
                        add_flag = True  # 是否添加的标记
                        if ":" in war or "see" in war.lower() or "other" in war.lower():
                            add_flag = False
                        elif "operator" in war.lower() or "below" in war.lower():
                            add_flag = False
                        elif war.startswith("-") or war.endswith("-") or war.startswith("."):
                            add_flag = False
                        elif war.endswith("by") or war.startswith("from") or war.endswith("in"):
                            add_flag = False
                        # 检查是否在之前出现过
                        for item in content:
                            if war.lower() in item.lower():
                                add_flag = False
                                break
                        if add_flag and war is not None and war.lower() not in discard_list:
                            if "/" in war and key != "Armament":
                                for item in war.split("/"):
                                    item = item.strip()
                                    if item is not None and item.lower() not in discard_list:
                                        content.append(item)
                            elif "," in war and key != "Armament":
                                for item in war.split(","):
                                    item = item.strip()
                                    if item is not None and item.lower() not in discard_list:
                                        content.append(item)
                            else:
                                content.append(war)
                    # 特殊处理 "-"
                    if "-" in content:
                        idx = content.index("-")
                        if idx - 1 < 0 or idx + 1 >= len(content):
                            content.remove("-")
                        else:
                            content[idx - 1] += content[idx] + content[idx + 1]
                            content.pop(idx)
                            content.pop(idx)
                    value = content
            # 关系
            if key in relation_list:
                processed_equipment["relation"][key] = value
            # 属性
            else:
                if value in ["-"]:
                    continue
                processed_equipment["attribute"][key] = value
        processed_equipment_list.append(processed_equipment)

    # 写入json文件
    print("内容筛选", content_num)
    print("名称筛选", name_num)
    print("重复筛选", repetition_num)
    with open(config.processed_data_path, 'w') as f:
        json.dump(processed_equipment_list, f)
    print(len(processed_equipment_list))

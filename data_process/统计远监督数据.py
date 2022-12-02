import json
from config import Config
import matplotlib.pyplot as plt

if __name__ == '__main__':
    config = Config()
    relation_type = dict()
    with open(config.all_train_path, 'r', encoding='utf8') as fp:
        data_list = json.load(fp)
    print("数据个数:", len(data_list))

    # 统计重叠类型数量
    Normal = 0
    EPO = 0
    SEO = 0
    for data in data_list:
        is_EPO = False
        is_SEO = False
        for idx, relationMention in enumerate(data["relationMentions"]):
            em1Text = relationMention["em1Text"]
            em2Text = relationMention["em2Text"]
            label = relationMention["label"]
            for relationMention2 in data["relationMentions"][idx + 1:]:
                em1Text2 = relationMention2["em1Text"]
                em2Text2 = relationMention2["em2Text"]
                label2 = relationMention2["label"]
                if em1Text == em1Text2 and em2Text == em2Text2:
                    is_EPO = True
                elif em1Text == em1Text2 or em2Text == em2Text2:
                    is_SEO = True
        if is_EPO:
            EPO += 1
        if is_SEO:
            SEO += 1
        if not is_EPO and not is_SEO:
            Normal += 1
    print("Normal:", Normal)
    print("EPO:", EPO)
    print("SEO:", SEO)

    # 统计不同关系类别的数量
    for data in data_list:
        for relationMention in data["relationMentions"]:
            label = relationMention["label"]
            relation_type[label] = relation_type.get(label, 0) + 1
    relation_type = dict(sorted(relation_type.items(), key=lambda i: i[-1], reverse=True))
    total_number = 0
    for key, value in relation_type.items():
        print(key, ":", value)
        total_number += value
    print("关系总数:", total_number)

    # 统计实体数量
    entity = dict()
    for data in data_list:
        for relationMention in data["relationMentions"]:
            label = relationMention["label"]
            em1Text = relationMention["em1Text"]
            em1Type = label.split("/")[1]
            em2Text = relationMention["em2Text"]
            em2Type = label.split("/")[2]
            if em1Type not in entity.keys():
                entity[em1Type] = set()
            entity[em1Type].add(em1Text)
            if em2Type not in entity.keys():
                entity[em2Type] = set()
            entity[em2Type].add(em2Text)

    total_number = 0
    for key, value in entity.items():
        print(key, ":", len(value))
        total_number += len(value)
    print("实体总数:", total_number)

    # 绘图
    plt.xticks(rotation=350)
    for relation, number in relation_type.items():
        plt.bar(relation.split("/")[3], number)
    plt.show()

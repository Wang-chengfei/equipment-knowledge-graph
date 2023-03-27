import json
from py2neo import *
from tqdm import tqdm
from config import Config
import random


def get_entity(entity, sentence):
    """
    检查实体是否在句子中
    若存在则实体在句子中的大小写
    否则返回None
    """
    real_sentence = sentence.split(" ")
    entity = entity.lower()
    sentence = sentence.lower()
    entity = entity.split(" ")
    sentence = sentence.split(" ")
    new_entity = ''
    n = len(entity)
    for i in range(len(sentence) - n + 1):
        if entity == sentence[i:i + n]:
            for item in real_sentence[i:i + n]:
                new_entity += item + ' '
            return new_entity.strip()
    return None


if __name__ == '__main__':
    config = Config()
    # 获取文本句子
    with open(config.processed_sentence_path, 'r', encoding='utf8') as fp:
        sentence_list = json.load(fp)
    print("句子总数：", len(sentence_list))

    # 连接neo4j 数据库
    graph = Graph('bolt://localhost:7687', auth=('neo4j', '123456'))
    node_matcher = NodeMatcher(graph)
    relationship_matcher = RelationshipMatcher(graph)

    # 获取实体名称集合
    node_list = node_matcher.match()
    entity_dict = dict()
    for node in node_list:
        entity_type = str(node.labels)[1:]
        entity_name = node["name"]
        if entity_type not in entity_dict.keys():
            entity_dict[entity_type] = []
        entity_dict[entity_type].append(entity_name)
    print(entity_dict)

    # 远程监督生成数据集
    data_list = []
    for sentence in tqdm(sentence_list, total=len(sentence_list)):
        data = dict()
        data["sentText"] = sentence
        data["relationMentions"] = []
        for entity1_type, entity1_list in entity_dict.items():
            if entity1_type != "equipment":
                continue
            for entity1_name in entity1_list:
                # 实体1在句子中
                if get_entity(entity1_name, sentence) is not None:
                    for entity2_type, entity2_list in entity_dict.items():
                        if entity2_type == "equipment":
                            continue
                        for entity2_name in entity2_list:
                            # 实体2在句子中
                            if get_entity(entity2_name, sentence) is not None:
                                node1 = node_matcher.match(entity1_type).where(name=entity1_name).first()
                                node2 = node_matcher.match(entity2_type).where(name=entity2_name).first()
                                relation_list = relationship_matcher.match(nodes=[node1, node2], r_type=None)
                                for relation in relation_list:
                                    triple = dict()
                                    # 取句子中的大小写作为实体的大小写形式
                                    em1Text = get_entity(entity1_name, sentence)
                                    em2Text = get_entity(entity2_name, sentence)
                                    # if get_entity(em1Text, em2Text) is not None or get_entity(em2Text, em1Text) is not None:
                                    #     continue
                                    triple["em1Text"] = em1Text
                                    triple["em2Text"] = em2Text
                                    relation_name = type(relation).__name__
                                    triple["label"] = "/" + entity1_type + "/" + entity2_type + "/" + relation_name
                                    data["relationMentions"].append(triple)
        if len(data["relationMentions"]) > 0:
            data_list.append(data)

    # 划分数据集
    random.seed(config.random_seed)
    random.shuffle(data_list)
    test_len = int(len(data_list) * config.test_ratio)
    if config.need_test:
        test_data = data_list[:test_len]
        valid_data = data_list[test_len:2 * test_len]
        train_data = data_list[2 * test_len:]
    else:
        test_data = []
        valid_data = data_list[:test_len]
        train_data = data_list[test_len:]
    print("test data number:", len(test_data))
    print("valid data number:", len(valid_data))
    print("train data number:", len(train_data))
    print("Overall:", len(data_list))

    # 句长统计
    sentence_len = dict()
    for sentence in data_list:
        word_list = sentence["sentText"].split(" ")
        word_len = len(word_list)
        sentence_len[word_len] = sentence_len.get(word_len, 0) + 1
    sentence_len = dict(sorted(sentence_len.items(), key=lambda i: i[0], reverse=True))
    print("句长统计", sentence_len)

    # 写入json文件
    with open(config.test_path, 'w') as f:
        json.dump(test_data, f)
    with open(config.valid_path, 'w') as f:
        json.dump(valid_data, f)
    with open(config.train_path, 'w') as f:
        json.dump(train_data, f)
    with open(config.all_train_path, 'w') as f:
        json.dump(data_list, f)

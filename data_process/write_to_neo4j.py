import json
from tqdm import tqdm
from py2neo import *
from config import Config


if __name__ == '__main__':
    config = Config()
    processed_data_path = config.processed_data_path
    relation2id_path = config.relation2id_path
    # 连接neo4j 数据库
    graph = Graph('bolt://localhost:7687', auth=('neo4j', '123456'))
    graph.delete_all()
    node_matcher = NodeMatcher(graph)
    with open(processed_data_path, 'r', encoding='utf8') as fp:
        equipment_list = json.load(fp)
    with open(relation2id_path, 'r', encoding='utf8') as fp:
        relation2id = json.load(fp)
    relation2entity = dict()
    for relation in relation2id:
        if relation == "None":
            continue
        head_entity = relation.split("/")[1]
        tail_entity = relation.split("/")[2]
        relation_type = relation.split("/")[3]
        relation2entity[relation_type] = tail_entity
    print(relation2entity)

    # 开始写入
    for equipment in tqdm(equipment_list, total=len(equipment_list)):
        entity_type = "equipment"
        equipment_node = node_matcher.match(entity_type).where(name=equipment["name"]).first()
        if equipment_node is None:
            equipment_node = Node(entity_type, name=equipment["name"])
            equipment_node.update(equipment["attribute"])
            graph.create(equipment_node)
        else:
            continue
        for key, value in equipment["relation"].items():
            # 处理字符串值
            if isinstance(value, str):
                entity_name = value
                entity_type = relation2entity[key]
                this_node = node_matcher.match(entity_type).where(name=entity_name).first()
                if this_node is None:
                    this_node = Node(entity_type, name=entity_name)
                    graph.create(this_node)
                this_relation = Relationship(equipment_node, key, this_node)
                graph.create(this_relation)
            # 处理列表值
            elif isinstance(value, list):
                for entity_name in value:
                    entity_type = relation2entity[key]
                    this_node = node_matcher.match(entity_type).where(name=entity_name).first()
                    if this_node is None:
                        this_node = Node(entity_type, name=entity_name)
                        graph.create(this_node)
                    this_relation = Relationship(equipment_node, key, this_node)
                    graph.create(this_relation)




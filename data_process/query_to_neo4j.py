from py2neo import *
from config import Config

if __name__ == '__main__':
    config = Config
    # 连接neo4j 数据库
    graph = Graph('bolt://localhost:7687', auth=('neo4j', '123456'))

    node_matcher = NodeMatcher(graph)
    relationship_matcher = RelationshipMatcher(graph)

    # node = node_matcher.match("company").where(name="then").first()
    # if node is not None:
    #     graph.delete(node)

    equipment_nodes = node_matcher.match("equipment")
    equipment_type_nodes = node_matcher.match("equipment_type")
    war_nodes = node_matcher.match("war")
    country_nodes = node_matcher.match("country")
    company_nodes = node_matcher.match("company")
    # armament_nodes = node_matcher.match("armament")
    nodes = node_matcher.match()
    print("equipment:", len(list(equipment_nodes)))
    print("equipment_type:", len(list(equipment_type_nodes)))
    print("war:", len(list(war_nodes)))
    print("country:", len(list(country_nodes)))
    print("company:", len(list(company_nodes)))
    # print("armament:", len(list(armament_nodes)))
    print("all:", len(nodes))

    print()
    for node in equipment_nodes:
        print(node["name"])
    # for node in nodes:
    #     print(node["name"])
    #     print(str(node.labels)[1:])

    # equipment_type_node = node_matcher.match("equipment").where(name="10TP").first()
    # relationship = relationship_matcher.match(nodes=[equipment_type_node], r_type=None)
    # relationship = list(relationship)
    # for relation in relationship:
    #     print(relation)
    #     print(type(relation).__name__)
    #     print(relation.end_node["name"])
    # print(relationship)


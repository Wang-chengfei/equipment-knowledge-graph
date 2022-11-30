from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher

# 连接neo4j 数据库
graph = Graph('bolt://localhost:7687', auth=('neo4j', '123456'))
graph.delete_all()
a = Node("Person", name="Alice")
b = Node("Person", name="Bob")
ab = Relationship(a, "KNOWS", b)
a['age'] = 20
b['age'] = 21
ab['time'] = '2017/08/31'
print(a, b, ab)
graph.create(ab)
graph.delete_all()

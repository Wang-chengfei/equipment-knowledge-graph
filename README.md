# 基于wikipedia数据的装备领域文本抽取与知识图谱构建（数据获取部分）



## 目录说明

- data_process  对爬取的数据进行处理（需要爬取完成后再运行）

  - data2relation.py  生成装备信息列表
  - data2sentence.py  生成句子列表，作为后续语料库使用
  - distant_supervise.py  使用远程监督方法生成数据集
  - query_to_neo4j.py  访问neo4j图数据库
  - split_train_data.py  将生成的数据集划分为训练集、测试集、验证集
  - write_to_neo4j.py  将data2relation.py生成的装备信息列表数据写入neo4j图数据库
  - 统计远程监督数据.py  统计distant_supervise.py生成的数据集

- discard  已废弃的文件，不作说明

- myData  已经生成好的训练集与测试集。测试集进行了人工校验，训练集进行一定校验。

- spider  爬虫部分

  - get_equipment_info.py  爬取wikipedia某一具体的装备url

  - get_equipment_list.py  爬取wikipedia装备列表页，获取装备url列表

  - run_spider.py  开始爬取

  - utils.py  一些通用函数

- config.py  配置文件



## 运行顺序

1. run_spider.py  从wikipeida爬取数据
2. data2relation.py, data2sentence.py  分别生成装备信息列表与句子列表
3. write_to_neo4j.py  将装备信息列表输入图数据库
4. distant_supervise.py  远程监督生成数据集
5. split_train_data.py  将生成的数据集划分为训练集、测试集、验证集
6. 统计远程监督数据.py  统计distant_supervise.py生成的数据集

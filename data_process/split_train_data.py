import json
import random
from config import Config

if __name__ == '__main__':
    config = Config()
    # 获取所有训练数据
    with open(config.all_train_path, 'r', encoding='utf8') as fp:
        data_list = json.load(fp)
    print("训练数据总数：", len(data_list))

    # 句长统计及筛选
    new_data_list = []
    sentence_len = dict()
    for sentence in data_list:
        word_list = sentence["sentText"].split(" ")
        word_len = len(word_list)
        if 8 <= word_len <= 80:
            new_data_list.append(sentence)
        sentence_len[word_len] = sentence_len.get(word_len, 0) + 1
    sentence_len = dict(sorted(sentence_len.items(), key=lambda i: i[0], reverse=True))
    print("句长统计", sentence_len)
    data_list = new_data_list

    # 去重
    new_data_list = []
    for data in data_list:
        new_data = dict()
        new_data["sentText"] = data["sentText"]
        new_data["relationMentions"] = []
        for idx, relationMention in enumerate(data["relationMentions"]):
            add_flag = True
            for relationMention2 in data["relationMentions"][:idx]:
                if relationMention["em1Text"] == relationMention2["em1Text"] and \
                    relationMention["em2Text"] == relationMention2["em2Text"] and \
                        relationMention["label"] == relationMention2["label"]:
                    add_flag = False
            if add_flag:
                new_data["relationMentions"].append(relationMention)
        if len(new_data["relationMentions"]) > 0:
            new_data_list.append(new_data)

    data_list = new_data_list

    # 划分数据集
    # random.seed(config.random_seed)
    # random.shuffle(data_list)
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

    # 写入json文件
    with open(config.test_path, 'w') as f:
        json.dump(test_data, f)
    with open(config.valid_path, 'w') as f:
        json.dump(valid_data, f)
    with open(config.train_path, 'w') as f:
        json.dump(train_data, f)

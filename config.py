import argparse


class Config(object):
    def __init__(self):
        # get init config
        args = self.__get_config()
        for key in args.__dict__:
            setattr(self, key, args.__dict__[key])

    @staticmethod
    def __get_config():
        parser = argparse.ArgumentParser()
        parser.description = 'config for models'

        # data directory
        parser.add_argument('--raw_data_path', type=str, default='../data/raw_data.json',
                            help='爬取到的原始数据')
        parser.add_argument('--raw_sentence_path', type=str, default='../data/raw_sentence.json',
                            help='爬取到的原始句子')
        parser.add_argument('--raw_data_example_path', type=str, default='../data/raw_data_example.json',
                            help='爬取到的原始示例数据')
        parser.add_argument('--url_equipment_list_path', type=str, default='../data/url_equipment_list.json',
                            help='将要爬取的装备url列表')
        parser.add_argument('--webpage_data_path', type=str, default='../data/webpage_data.json',
                            help='网页数据')
        parser.add_argument('--webpage_bingSearch_path', type=str, default='../data/webpage_bingSearch.json',
                            help='bing搜索结果')
        parser.add_argument('--webpage_sentence_path', type=str, default='../data/webpage_sentence.json',
                            help='采集句子的网页数据')
        parser.add_argument('--bingSearch_result_path', type=str, default='../data/bingSearch_result.json',
                            help='用于爬取句子的url列表')
        parser.add_argument('--relation2id_path', type=str, default='../data/relation2id.json',
                            help='关系与id对应文件')
        parser.add_argument('--processed_data_path', type=str, default='../data/processed_data.json',
                            help='经过处理，生成装备的属性和关系字典，并去除原始数据中的句子')
        parser.add_argument('--processed_sentence_path', type=str, default='../data/processed_sentence.json',
                            help='经过处理，生成所有的句子，并去除原始数据中的装备属性等信息')
        parser.add_argument('--all_train_path', type=str, default='../data/all_train.json',
                            help='所有的训练数据')
        parser.add_argument('--train_path', type=str, default='../data/train.json',
                            help='train data path')
        parser.add_argument('--test_path', type=str, default='../data/test.json',
                            help='test data path')
        parser.add_argument('--valid_path', type=str, default='../data/valid.json',
                            help='valid data path')

        # spider
        parser.add_argument('--wikipedia_url', type=str, default='https://en.wikipedia.org',
                            help='wikipedia url')
        parser.add_argument('--example_url', type=str, default='https://en.wikipedia.org/wiki/Arjun (tank)',
                            help='示例装备url')
        parser.add_argument('--url_list', type=list,
                            default=["https://en.wikipedia.org/wiki/List_of_military_vehicles",
                                     "https://en.wikipedia.org/wiki/List_of_armored_fighting_vehicles_of_the_Soviet_Union",
                                     "https://en.wikipedia.org/wiki/List_of_combat_vehicles_of_World_War_I",
                                     "https://en.wikipedia.org/wiki/List_of_interwar_armoured_fighting_vehicles",
                                     "https://en.wikipedia.org/wiki/List_of_military_vehicles_of_World_War_II",
                                     "https://en.wikipedia.org/wiki/List_of_prototype_World_War_II_combat_vehicles",
                                     "https://en.wikipedia.org/wiki/List_of_armoured_fighting_vehicles_of_World_War_II",
                                     "https://en.wikipedia.org/wiki/List_of_main_battle_tanks_by_generation",
                                     "https://en.wikipedia.org/wiki/List_of_armoured_fighting_vehicles_by_country",
                                     "https://en.wikipedia.org/wiki/List_of_modern_armoured_fighting_vehicles",
                                     "https://en.wikipedia.org/wiki/List_of_Sd.Kfz._designations",
                                     "https://en.wikipedia.org/wiki/List_of_main_battle_tanks_by_country",
                                     "https://en.wikipedia.org/wiki/List_of_Polish_armoured_fighting_vehicles",
                                     "https://en.wikipedia.org/wiki/List_of_armoured_fighting_vehicles_of_Ukraine",
                                     "https://en.wikipedia.org/wiki/List_of_tanks_of_the_United_Kingdom",
                                     "https://en.wikipedia.org/wiki/List_of_FV_series_military_vehicles",
                                     "https://en.wikipedia.org/wiki/List_of_the_United_States_military_vehicles_by_model_number",
                                     ],
                            help='爬取的初始页面列表')
        parser.add_argument('--waiting_time', type=float, default=0,
                            help='爬取页面等待时间')
        parser.add_argument('--long_waiting_time', type=float, default=5,
                            help='爬取页面失败后的等待时间')
        parser.add_argument('--save_num', type=int, default=100,
                            help='每爬取多少个保存一次数据')

        # data process
        parser.add_argument('--normalize_signature', type=str, default='NFKC',
                            help='unicodedata.normalize(normalize_signature, text)')
        parser.add_argument('--test_ratio', type=float, default=0.1,
                            help='测试数据比例')
        parser.add_argument('--random_seed', type=int, default=2022,
                            help='随机种子')

        args = parser.parse_args()
        return args

    def print_config(self):
        for key in self.__dict__:
            print(key, end=' = ')
            print(self.__dict__[key])


if __name__ == '__main__':
    config = Config()
    config.print_config()

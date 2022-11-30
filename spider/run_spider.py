from get_equipment_list import *
from get_equipment_info import *
from config import Config


def run(config):
    # 获取需要爬取的装备url
    url_equipment_list = get_equipment_list(config)
    print(len(url_equipment_list))

    # 去除已经爬取的装备url，并加载已经爬取的数据
    equipment_list = []
    if os.path.exists(config.raw_data_path):
        with open(config.raw_data_path, 'r', encoding='utf8') as fp:
            equipment_list = json.load(fp)
            print("已爬取", len(equipment_list), "条装备数据")
        new_equipment_list = []
        # 去除重复的数据
        for idx, equipment in enumerate(equipment_list):
            url_count = 0
            for item in equipment_list:
                if item["wiki_url"] == equipment["wiki_url"]:
                    url_count += 1
            if url_count == 1:
                new_equipment_list.append(equipment)
        equipment_list = new_equipment_list
        print("去重后，还有", len(equipment_list), "条装备数据")
        for equipment in equipment_list:
            url_equipment_list.remove(equipment["wiki_url"])

    print("准备爬取的装备url列表长度：", len(url_equipment_list))

    # 开始爬取
    for url_equipment in tqdm(url_equipment_list, total=len(url_equipment_list)):
        try:
            equipment = get_equipment_info(url=url_equipment, config=config)
        except:
            equipment = None
            print("爬取", url_equipment, "出现异常，稍后继续爬取...")
            time.sleep(config.long_waiting_time)
        if equipment is not None:
            equipment_list.append(equipment)
            # 每爬取到save_num个时保存一次数据
            if len(equipment_list) % config.save_num == 0:
                with open(config.raw_data_path, 'w') as f:
                    json.dump(equipment_list, f)
                print("数据已保存，已爬取", len(equipment_list), "条装备数据")
        # 爬取一次等待一定时间
        time.sleep(config.waiting_time)

    print("完成！！！爬取到的的装备列表长度：", len(equipment_list))

    # 写入json文件
    with open(config.raw_data_path, 'w') as f:
        json.dump(equipment_list, f)
    print("数据已写入至：", config.raw_data_path)


if __name__ == '__main__':
    config = Config()
    run(config)

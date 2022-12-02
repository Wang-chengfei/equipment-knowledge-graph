from lxml import etree
from utils import *
from config import Config


if __name__ == '__main__':
    config = Config()
    url = "https://en.wikipedia.org/wiki/Land_Rover_Wolf"
    page_text = get_page_text(url=url, webpage_data_path=config.webpage_sentence_path)
    tree = etree.HTML(page_text)
    sentence_list = tree.xpath('//text()')
    document = ''
    for sentence in sentence_list:
        document += sentence
    print(document)

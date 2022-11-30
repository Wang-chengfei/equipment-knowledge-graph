from lxml import etree
from utils import *
from config import Config
from py2neo import *

if __name__ == '__main__':
    config = Config()
    url = "https://en.wikipedia.org/wiki/10TP"
    page_text = get_page_text(url=url, webpage_data_path=config.webpage_data_path)
    tree = etree.HTML(page_text)
    sentence_list = tree.xpath('//p//text()')
    document = ''
    for sentence in sentence_list:
        document += sentence
    print(document)

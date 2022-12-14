import json
import unicodedata
import re
from config import Config
from tqdm import tqdm
import spacy


def clean_str(string):
    """
    清洗句子
    """
    # string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r";", " ; ", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " ( ", string)
    string = re.sub(r"\)", " ) ", string)
    string = re.sub(r"\?", " ? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip()


if __name__ == '__main__':
    config = Config()
    nlp = spacy.load("en_core_web_sm")
    sentence_list = []
    with open(config.raw_sentence_path, 'r', encoding='utf8') as fp:
        document_list = json.load(fp)

    # 开始处理
    for document in tqdm(document_list, total=len(document_list)):
        sentences = document["document"]
        sentences = unicodedata.normalize(config.normalize_signature, sentences)
        sentences = re.sub(r"\[.*?\]", "", sentences)
        sentences = re.sub(r"\(.*?\)", "", sentences)
        sentences = re.sub(r"\{.*?\}", "", sentences)
        sentences = re.sub(r"\s{2,}", " ", sentences)
        print(sentences)
        sentences = nlp(sentences).sents
        for sentence in sentences:
            # print(sentence.text)
            sentence = sentence.text
            # sentence = unicodedata.normalize(config.normalize_signature, sentence)
            sentence = re.sub(r"\[.*?\]", "", sentence)
            sentence = re.sub(r"\(.*?\)", "", sentence)
            sentence = clean_str(sentence)
            sentence = sentence.strip() + " ."
            sentence_list.append(sentence)

    print("去重前：", len(sentence_list))
    sentence_list = list(dict.fromkeys(sentence_list))
    print("去重后：", len(sentence_list))

    # 句长统计
    sentence_len = dict()
    for sentence in sentence_list:
        word_list = sentence.split(" ")
        word_len = len(word_list)
        sentence_len[word_len] = sentence_len.get(word_len, 0) + 1
    sentence_len = dict(sorted(sentence_len.items(), key=lambda i: i[0], reverse=True))
    print("句长统计", sentence_len)

    # 写入json文件
    with open(config.processed_sentence_path, 'w') as f:
        json.dump(sentence_list, f)

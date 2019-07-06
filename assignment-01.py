import random
import pandas as pd
import re
from collections import Counter
import jieba
from functools import reduce
from operator import add, mul
import numpy as np


# *******************************句子生成器*******************************


def create_grammar(grammar_str, split='=', line_split='\n'):
    grammar = {}
    for line in grammar_str.split(line_split):
        if not line.strip():
            continue
        exp, stmt = line.split(split)
        grammar[exp.strip()] = [s.split() for s in stmt.split('|')]
    return grammar


choice = random.choice


def generate(gram, target):
    if target not in gram:
        return target  # means target is a terminal expression
    expaned = [generate(gram, t) for t in choice(gram[target])]
    return ''.join([e if e != '/n' else '\n' for e in expaned if e != 'null'])


def generate_n(gram, target, n):
    sentences = []
    for i in range(n):
        sentences.append(generate(gram, target))
    return sentences


human = """
 human = 自己 寻找 活动
 自己 = 我 | 俺 | 我们 
 寻找 = 看看 | 找找 | 想找点
 活动 = 乐子 | 玩的
 """

host = """
host = 寒暄 报数 询问 业务相关 结尾
报数 = 我是 数字 号 ,
数字 = 单个数字 | 数字 单个数字 
单个数字 = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 
寒暄 = 称谓 打招呼 | 打招呼
称谓 = 人称 ,
人称 = 先生 | 女士 | 小朋友
打招呼 = 你好 | 您好 
询问 = 请问你要 | 您需要
业务相关 = 玩玩 具体业务
玩玩 = 耍一耍 | 玩一玩
具体业务 = 喝酒 | 打牌 | 打猎 | 赌博
结尾 = 吗？"""


# print(create_grammar(human))
# print(generate(create_grammar(human), 'human'))
# print(generate_n(create_grammar(host), 'host', 10))

# *******************************语言模型训练*******************************
# 文本清洗
filename = '~/06.30_lesson01/movie_comments.csv'

content = pd.read_csv(filename, encoding='utf-8', low_memory=False)

articles = content['comment'].tolist()

# print(len(articles))  # 261497


def token(string):
    return re.findall('\w+', string)


articles_clean = [''.join(token(str(a)))for a in articles]

# print(len(articles_clean))
with open('~/06.30_lesson01/movie_comments_clean.csv', 'w') as f:
    for a in articles_clean:
        f.write(a + '\n')


# 语言模型
def cut(string):
    return list(jieba.cut(string))


token = []

for i, line in enumerate((open('/Users/honglian.lhl/06.30_lesson01/movie_comments_clean.csv'))):
    if i % 100 == 0:
        print(i)
    if i > 100000:
        break
    token += cut(line)

words_count = Counter(token)

token = [str(t) for t in token]

token_2_gram = [''.join(token[i:i+2]) for i in range(len(token[:-2]))]

words_count_2 = Counter(token_2_gram)


def prob_2(word1, word2):
    if word1 + word2 in words_count_2:
        return words_count_2[word1+word2] / len(token_2_gram)
    else:
        return 1 / len(token_2_gram)


# *******************************获取优质语言*******************************
def get_probability(sentence):
    words = cut(sentence)
    sentence_pro = 1
    for i, word in enumerate(words[:-1]):
        next_ = words[i + 1]

        probability = prob_2(word, next_)

        sentence_pro *= probability

    return sentence_pro


def generate_best(gram, target, n):
    sentences = []
    for sen in generate_n(create_grammar(gram), target, n):
        print(sen, get_probability(sen))
        sentences.append((sen, get_probability(sen)))
    return sorted(sentences, key=lambda x: x[1], reverse=True)[0][0]


# generate_best(host, 'host', 10)
print(generate_best(host, 'host', 10))

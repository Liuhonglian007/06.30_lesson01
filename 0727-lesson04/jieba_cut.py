import jieba
import os


# jieba.cut的默认参数只有三个,jieba源码如下
# cut(self, sentence, cut_all=False, HMM=True)
# 分别为:输入文本 是否为全模式分词 与是否开启HMM进行中文分词

# 原始文件中一行是一段，一行一行读取，进行分词，分词之后存入新的文件，一行仍是一段
# 分词之后，进行停非中文字符的处理

class Mysentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), encoding='utf-8'):
                if len(line) > 0:
                    yield [segment.strip() for segment in jieba.cut(line.strip()) if len(segment) > 0]


def is_ustr(instr):
    out_str = ''
    for index in range(len(instr)):
        if is_uchar(instr[index]):
            out_str = out_str + instr[index].strip()
    return out_str


def is_uchar(uchar):
    if u'\u4e00' <= uchar <= u'\u9fff':
        return True


if __name__ == '__main__':
    dirname = '/Users/honglian.lhl/2019-nlp-assignments/0727-lesson04/wiki_extracted/AA/wiki_jian'

    # 进行jieba分词,sentences是一个生成器，调用一次读一行数据
    sentences = Mysentences(dirname)

    # 分词结果写入文件
    f = open('/Users/honglian.lhl/2019-nlp-assignments/0727-lesson04/wiki_extracted/AA/wiki_jieba.txt', 'w', encoding='utf-8')
    i = 0
    j = 0
    for sentence in sentences:
        if len(sentence) > 0:
            output = ''
            for d in sentence:
                if len(is_ustr(d)) > 0:
                    # 只保留中文词，并拼接成空格分隔de句子
                    output += is_ustr(d).strip() + " "
            f.write(output.strip())
            f.write('\r\n')
            i += 1
            if i % 10000 == 0:
                j += 1
                print(u'已分词：%s万行' % j)
    f.close()

import logging
from gensim.models import Word2vec
from gensim.models.word2vec import LineSentence

if __name__ == '__main__':

    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s",level=logging.INFO)

    infile='/Users/honglian.lhl/2019-nlp-assignments/0727-lesson04/wiki_extracted/AA/wiki_jieba.txt'
    vec_outfile1='/Users/honglian.lhl/2019-nlp-assignments/0727-lesson04/wiki.model'
    vec_outfile2='/Users/honglian.lhl/2019-nlp-assignments/0727-lesson04/wiki.vector'

    sentences=LineSentence(infile)
    model=Word2vec(sentences,size=100,window=5,min_count=5)#size为词向量的维度大小

    model.save(vec_outfile1)
    model.wv.save_word2vec_format(vec_outfile2,binary=false)

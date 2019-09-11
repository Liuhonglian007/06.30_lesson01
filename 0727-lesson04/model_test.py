from gensim.models import Word2vec

if __name__ == '__main__':

    model = Word2vec.load('/Users/honglian.lhl/2019-nlp-assignments/0727-lesson04/wiki.model')

    word1 = u'计算机'
    word2 = u'人工智能'
    words = [word1, word2]

    for word in words:
        if word in model:
            print(u"'%s'的词向量为：" % word)
            print(model[word])
        else:
            print(u'单词不在字典中!\n')

        result = model.most_similar(word, topn=10)
        print(u"与'%s'最相似d词为：" % word)
        for e in result:
            print('%s:%f' % (e[0], e[1]))

    print(u"\n'%s'与'%s'的相似度为：%f" % (word1, word2, model.similarity(word1, word2)))
    print(u"\n'早餐 晚餐 午餐 中心'中的离群词为： ")
    print(model.doesnt_match(u"早餐 晚餐 午餐 中心".split()))

    print(u"\n与'%s'最相似，而与'%s'最不相似的词为： " % (word1, word2))
    temp = (model.most_similar(positive=[word1], negative=[word2], topn=1))
    print('%s: %s' % (temp[0][0], temp[0][1]))

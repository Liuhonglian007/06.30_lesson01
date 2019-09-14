from gensim.models import Word2Vec
import random
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels_all = []
    labels = []
    tokens = []

    for word in model.wv.vocab:
        labels_all.append(word)

    # 随机选取500个点，进行可视化
    labels = random.sample(labels_all, 500)
    for word in labels:
        tokens.append(model[word])

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2000, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()


if __name__ == '__main__':
    model = Word2Vec.load('/Users/honglian.lhl/2019-nlp-assignments/0727-lesson04/wiki.model')
    tsne_plot(model)

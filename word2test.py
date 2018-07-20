from gensim.models import word2vec

model = word2vec.Word2Vec.load('kingyo.model')

for word in ['金魚', '生命', '作る']:
    words = model.most_similar(positive=[word])
    n = [w[0] for w in words]
    print(word, '=', ','.join(n))


test = word2vec.Word2Vec.load('kingyo.model')
# 金魚＋生命 - 作る =
test.most_similar(positive=['金魚', '生命'], negative=['作る'])[0]
t= [w[0] for w in words]
print(test, '=', ','.join(t))
from gensim.test.utils import get_tmpfile
from tools import get_data_for_word2vec
from gensim.models import Word2Vec
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity

data_for_word2vec = '../data_for_word2vec/data'
# if os.path.exists(data_for_word2vec):
#     os.remove(data_for_word2vec)
# get_data_for_word2vec('../apk_data/benign/',data_for_word2vec)
# get_data_for_word2vec('../apk_data/unbenign/',data_for_word2vec)

# texts = np.loadtxt(data_for_word2vec,dtype=str,delimiter='\n')
# texts = [s.split(' ') for s in texts]
# vocabulary_size = len(set([i for x in texts for i in x]))
# path = get_tmpfile("word2vec.model")
# model = Word2Vec(texts, size=100, window=5, min_count=1, workers=4)
# model.save("word2vec.model")
model = Word2Vec.load("word2vec.model")
vector = model.wv['iget-object']
print(vector)
a=1


from transformers import AutoTokenizer
from tokenizers import Tokenizer
import pandas as pd

raw_inputs = open("../data/reviews.txt").readlines()

"""tokenizer = Tokenizer.from_pretrained("bert-base-uncased")
inputs = tokenizer.encode(raw_inputs)



print(inputs.tokens)
print(inputs.attention_mask)
"""
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

tfidf_vectorizer=TfidfVectorizer(use_idf=True)
tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(raw_inputs)
first_vector_tfidfvectorizer=tfidf_vectorizer_vectors[1]
#df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=tfidf_vectorizer.get_feature_names_out(), columns=["tfidf"])
df = pd.DataFrame(tfidf_vectorizer_vectors.sum(axis=0).T, index=tfidf_vectorizer.get_feature_names_out(), columns=["tfidf"])
print(df.sort_values(by=["tfidf"],ascending=False).head(45))
print(df.shape)


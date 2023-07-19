import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

tfidf_vectorizer=TfidfVectorizer(use_idf=True)
tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(raw_inputs)
first_vector_tfidfvectorizer=tfidf_vectorizer_vectors[1]
#df = pd.DataFrame(first_vector_tfidfvectorizer.T.todense(), index=tfidf_vectorizer.get_feature_names_out(), columns=["tfidf"])
df = pd.DataFrame(tfidf_vectorizer_vectors.sum(axis=0).T, index=tfidf_vectorizer.get_feature_names_out(), columns=["tfidf"])
print(df.sort_values(by=["tfidf"],ascending=False).head(45))
print(df.shape)

def
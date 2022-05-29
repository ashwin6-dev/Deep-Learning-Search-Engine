from sentence_transformers import SentenceTransformer
import pickle
import numpy as np
from sklearn.neighbors import NearestNeighbors

model = SentenceTransformer('sentence-transformers/stsb-roberta-base-v2')

kmeans = pickle.load(open("cluster.save", 'rb'))
buckets = pickle.load(open("buckets.save", 'rb'))

while True:
    query = input("Search: ")
    encoded_query = model.encode(query)
    encoded_query = np.expand_dims(encoded_query, axis=0)
    bucket = kmeans.predict(encoded_query)
    bucket = int(bucket.squeeze())
    embeddings = []

    for result in buckets[bucket]:
        embeddings.append(result["content"])
    embeddings = model.encode(embeddings)
    neigh = NearestNeighbors(n_neighbors=10)
    neigh.fit(embeddings)
    indexes = neigh.kneighbors(encoded_query, return_distance=False)

    for index in indexes.T:
      doc = buckets[bucket][int(index.squeeze())]
      print (doc["title"], doc["url"])
      print ("")
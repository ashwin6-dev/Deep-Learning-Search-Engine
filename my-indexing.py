from tinydb import TinyDB
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

model = SentenceTransformer('sentence-transformers/stsb-roberta-base-v2')
db = TinyDB("results.json")

contents = []

for record in db:
    content = record["content"]
    contents.append(content)

embeddings = model.encode(contents)

kmeans = KMeans(n_clusters=3)
kmeans.fit(embeddings)
buckets = {}

for record, label in zip(db, kmeans.labels_):
    if label not in buckets:
        buckets[label] = []

    buckets[label].append(dict(record)) 
    
import pickle

pickle.dump(kmeans, open("kmeans-model.save", "wb"))
pickle.dump(buckets, open("buckets.save","wb"))
from tinydb import TinyDB
from sentence_transformers import SentenceTransformer
from annoy import AnnoyIndex

model = SentenceTransformer('sentence-transformers/stsb-roberta-base-v2')
db = TinyDB("results.json")

index = AnnoyIndex(768, "euclidean")
index.load("index.ann")

while True:
    query = input("Search: ")

    vec = model.encode(query)
    indexes = (index.get_nns_by_vector(vec, 20))
    all_db = db.all()

    for i in indexes:
        print (all_db[i]["title"], all_db[i]["url"])
        print ("")
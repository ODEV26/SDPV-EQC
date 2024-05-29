from pymongo import MongoClient

client = MongoClient("mongodb+srv://of91778:of91778@cluster3.l7a1a5q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster3")
db = client["registros"]
db2 = client["usuarios"]
collection_1 = db["datos"]
collection_2 = db["salida"]
collection_3 = db2["administradores"]
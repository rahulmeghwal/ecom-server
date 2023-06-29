import pandas as pd
from pymongo import MongoClient
import json
import urllib.parse

db_name = 'INVENTORY'
coll_name = 'products'
username = urllib.parse.quote_plus('mongodbuser')
password = urllib.parse.quote_plus('p@ssw0rd')
client = MongoClient('mongodb://%s:%s@3.84.157.245:27017/%s' % (username, password,db_name))
db = client[db_name]
coll = db[coll_name]

coll.drop()

csv_path = '/Users/rahulmeghwal/my-ecom/data/Myntra_Data_Cleansed_4k.csv'
data = pd.read_csv(csv_path)
payload = json.loads(data.to_json(orient='records'))
coll.remove()
coll.insert(payload)
print(coll.count())
client.close()

# S	M	L	XL	XXL	3XL	S|M	M|L	L|XL|XXL	S|M|L|XL|XXL|3XL	S|M|L	M|L|XL	S|M|L|XL	M|L|XL|XXL											
from flask import Flask,request
from flask import jsonify
from pymongo import MongoClient
import json
import urllib.parse
from bson import json_util
from flask_cors import CORS

product_attributes = {'brand'           :1,
                      'size'            :1,
                      'dominant_color'  :1, 
                      'title'           :1, 
                      'variant_price'   :1,
                      'product_id'      :1,
                      'ideal_for'       :1,
                      'images'          :1,
                      'product_type'    :1,
                      'variant_compare_at_price':1
                    }

products_per_page = 100

db_name = "INVENTORY"
product_collection = "products"
cart_collection = "cart"

username = urllib.parse.quote_plus('mongodbuser')
password = urllib.parse.quote_plus('p@ssw0rd')

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = 'mongodb://%s:%s@3.84.157.245:27017/%s' % (username, password,db_name)
mongo = MongoClient(app.config["MONGO_URI"])

@app.route("/getProducts/<page_no>")
def getProducts(page_no):
    page_no = int(page_no)
    skip_products = products_per_page * (page_no - 1) 
    args = request.args.to_dict()
    
    records = []
    searchQuery = {}
    if('searchString' in args and len(args['searchString']) > 0):
        searchRegex = ".*"
        for search in args['searchString'].split(' '):
            searchRegex = searchRegex + search + ".*"

        searchQuery['body'] = { '$regex' : searchRegex}
    
    if('brand' in args and len(args['brand']) > 0):
        searchQuery['brand'] = { '$in' : args['brand'].split(',')}
        
    records = mongo[db_name][product_collection].find(searchQuery,product_attributes).skip(skip_products).limit(products_per_page)
    
    documents = [document for document in records]
    response = json.loads(json_util.dumps(documents))

    return response



@app.route("/getProductDetails/<product_id>")
def getProductDetails(product_id):
    product_id = int(product_id)
    records = mongo[db_name][product_collection].find({'product_id': product_id})
    documents = [document for document in records]
    return json.loads(json_util.dumps(documents))

app.run(host="0.0.0.0", port=8080)

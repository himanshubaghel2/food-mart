import json
from flask import Flask, jsonify,request, Response
import pymongo


app = Flask(__name__)


client = pymongo.MongoClient('mongo.servers.nferx.com',username='himanshu.b',password='9jm38mhm594v1s7')
mydb = client["himanshu"]
mycol = mydb["fooditems"]   


@app.route('/')
def index():
    return ("Load food items and get food items ")


@app.route('/load',methods=["GET"])
def loadMachine():
    file = open("data.json")
    data = json.load(file)
    mycol.insert_many(data["items"])
    return("Done")


@app.route('/show',methods=["GET"])
def showItems():
    mydoc = mycol.find()
    list_cur = list(mydoc)
    jss=json.dumps(list_cur , default=str)
    js=json.loads(jss)
    return (jsonify(js))

@app.route('/fetch',methods=["GET"])
def fetchItems():
    item = request.args.get('item')
    amount = request.args.get('amount')
    amount=int(amount)
    quantity = request.args.get('quantity')
    quantity=int(quantity)
    myquery = {"item": item}
    mydoc = mycol.find(myquery)

    for x in mydoc:
        pass

    mydoc = mycol.find(myquery)
    results = list(mydoc)
    if len(results)==0:
        return("Item not found")    
    
    
    price=x['price']
    available=x['quantity']

    if (quantity > available) or (amount < price*quantity):
        return("Sorry")

    myquery = {"item": item}
    newvalues = { "$set": { "quantity": (available-quantity) } }
    mycol.update_one(myquery, newvalues)

    a=str(item)+str(amount)+str(quantity)
    return("Please take "+ str(quantity)+" "+str(item)+"(s) and "+str(amount - price*quantity)+ "Rs back")     



if __name__=="__main__":
    app.run( host='0.0.0.0', port=80, debug=True)    
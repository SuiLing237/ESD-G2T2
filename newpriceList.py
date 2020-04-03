# !/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import sys
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/price_list' # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

paymentURL = "http://localhost:5001/payment"

class Price (db.Model):
    __tablename__ = "price_list"

    medicineID = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(64), nullable=False)
    medicine_price = db.Column(db.Float, nullable=False)

    def __init__(self, medicineID, medicine_name, medicine_price):
        self.medicineID = medicineID
        self.medicine_name = medicine_name
        self.medicine_price = medicine_price
    
    def json(self):
         return {"medicineID": self.medicineID, "medicine_name": self.medicine_name, "medicine_price": self.medicine_price}

@app.route("/")
def home():
    return "test"

# @app.route("/pricelist/", methods=['POST'])
# def receiveOrder(): # order = medicineID
    # # Check if the order contains valid JSON
    # order = None
    # if request.is_json:
    #     order = request.get_json()
    # else:
    #     order = request.get_data()
    #     print("Received an invalid order:")
    #     print(order)
    #     replymessage = json.dumps({"message": "Order should be in JSON", "data": order}, default=str)
    #     return replymessage, 400 # Bad Request
    # print("Received an order by " + __file__)
    # result = processOrder(order)
    # print() # print a new line feed as a separator
    # # reply to the HTTP request
    # replymessage = json.dumps(result, default=str)
    # if result["status"]:
    #     return replymessage, 200 #return the json along with the http status code 200
    # else:
    #     return replymessage, 501 #return the json along with the http status code 501

@app.route("/getMedicineName/", methods=['GET'])
def getMedicineName():
    list_of_medicine = Price.query.all()
    return jsonify({"medicine": [m.json() for m in list_of_medicine]})

@app.route("/price", methods=['POST'])
def receiveOrder():
    # Check if the order contains valid JSON
    # order = None
    result = 0
    if request.is_json:
        order = request.get_json()
        result = processOrder(order)
    else:
        order = request.get_data()
        print("Received an invalid order:")
        print(order)
        replymessage = json.dumps({"message": "Order should be in JSON", "data": order}, default=str)
        return replymessage, 400 # Bad Request

    # print() # print a new line feed as a separator
    # # reply to the HTTP request
    # replymessage = json.dumps(result, default=str)
    # if result["status"]:
    #     return replymessage, 200 #return the json along with the http status code 200
    # else:
    #     return replymessage, 501 #return the json along with the http status code 501

    return json.dumps(result, default=str)

def processOrder(order):
    print("Processing an order:")
    total_price = 0
    for medicine in order["prescription"]:
        med_id = medicine["medicineID"]
        med_info = find_price_by_med_id(med_id) #retrieve price from data base

        med_price = med_info["medicine_price"]
        price = med_price * medicine["medicine_quantity"]


        total_price += price
    print("Total Price is:")
    print('$' + str(total_price))
    return total_price

# @app.route("/find_by_order_id/<string:order_id>")
def find_price_by_med_id(med_id):
    med_details = Price.query.filter_by(medicineID=med_id).first()
    if med_details:
        return med_details.json()
    return {'message': 'Medicine not found for id ' + str(med_id)}, 404

def send_price(price):
    price = json.loads(json.dumps(price, default = str))

    #send to medicine microservice
    r = requests.post(paymentURL, json = price)
    print("Price sent to paypal.")

    

    
if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    # print("This is flask for " + os.path.basename(__file__) + ": shipping for an order...")
    # app.run(host='0.0.0.0', port=5002, debug=True)
    app.run(port=5006, debug=True)

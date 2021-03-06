# !/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import sys
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/price_list' # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)



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

@app.route("/getMedicineName/", methods=['GET'])
def getMedicineName():
    list_of_medicine = Price.query.all()
    return jsonify({"medicine": [m.json() for m in list_of_medicine]})

@app.route("/price", methods=['POST'])
def receiveOrder():
    # Check if the order contains valid JSON
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

    return json.dumps(result, default=str)

def processOrder(order):
    print("Processing an order:")
    print(order)
    print("******")
    total_price = 0
    patientID = order["patientID"]
    bookingID = order["bookingID"]

    for medicine in order["prescription"]:
        med_id = medicine["medicineID"]
        med_info = find_price_by_med_id(med_id) #retrieve price from data base

        med_price = med_info["medicine_price"]
        price = med_price * medicine["medicine_quantity"]


        total_price += price
    print("Total Price is:")
    print('$' + str(total_price))
    send_price(patientID, bookingID, total_price)
    return total_price

def find_price_by_med_id(med_id):
    med_details = Price.query.filter_by(medicineID=med_id).first()
    if med_details:
        return med_details.json()
    return {'message': 'Medicine not found for id ' + str(med_id)}, 404

def send_price(patientID, bookingID, total_price):
    payment = {"total_price": total_price}
    message = jsonify(payment)
    print(payment)
    print(payment)
    print("******")
    print(type(message))
    paymentURL = "http://127.0.0.1:5003/create_payment" +"/" + str(patientID) +"/" +str(bookingID)
    #send to medicine microservice
    r = requests.post(paymentURL, json = payment)
    print(r.status_code, r.text, sep='\n')
    return "ok"


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    app.run(port=5006, debug=True)

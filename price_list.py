
#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import json
import sys
import pika
import os
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/order'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
CORS(app)

hostname = "localhost" # default hostname
port = 5672 # default port
# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
    # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
channel = connection.channel()
# set up the exchange if the exchange doesn't exist
exchangename="prescription_direct"
channel.exchange_declare(exchange=exchangename, exchange_type='direct')

class PriceList (db.Model):
    __tablename__ = 'price_list'
 
    med_id = db.Column(db.Integer, primary_key=True)
    med_name = db.Column(db.String(32), nullable=False)
    med_cost = db.Column(db.Float, nullable=False)

    def json(self):
        dto = {
            'medicineID': self.med_id, 
            'medicine_name': self.med_name, 
            'medicine_cost': self.med_cost
        }

        dto['order_item'] = []
        for oi in self.order_item:
            dto['order_item'].append(oi.json())

        return dto

def receivePrescription():
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="price_list", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='prescription.price_list') # bind the queue to the exchange via the key

    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True) # 'auto_ack=True' acknowledges the reception of a message to the broker automatically, so that the broker can assume the message is received and processed and remove it from the queue
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    # print("Received an order by " + __file__)
    result = calculateCost(json.loads(body))
    # print processing result; not really needed
    json.dump(result, sys.stdout, default=str) # convert the JSON object to a string and print out on screen
    print() # print a new line feed to the previous json dump
    print() # print another new line as a separator

def calculateCost(prescription_details):
    getMedicinePrice =

    # Can do anything here. E.g., publish a message to the error handler when processing fails.
    resultstatus = bool(random.getrandbits(1)) # simulate success/failure with a random True or False
    result = {'status': resultstatus, 'message': 'Simulated random shipping result.', 'order': order}
    resultmessage = json.dumps(result, default=str) # convert the JSON object to a string
    if not resultstatus: # inform the error handler when shipping fails
        print("Failed shipping.")
        # send the message to the eror handler
        channel.queue_declare(queue='errorhandler', durable=True) # make sure the queue used by the error handler exist and durable
        channel.queue_bind(exchange=exchangename, queue='errorhandler', routing_key='shipping.error') # make sure the queue is bound to the exchange
        channel.basic_publish(exchange=exchangename, routing_key="shipping.error", body=resultmessage,
            properties=pika.BasicProperties(delivery_mode = 2) # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
        )
    else:
        print("OK shipping.")
    return result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
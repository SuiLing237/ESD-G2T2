# import requests
# import urllib.request
# import urllib.parse
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# For email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# for amqp
import pika
import json
import os
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient' # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


hostname = "localhost"
port = 5672
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
channel = connection.channel()
exchangename="patient_direct"
channel.exchange_declare(exchange=exchangename, exchange_type='direct')


def send_email(patient_name, patient_email):
    MY_ADDRESS = 'maple_0309@hotmail.com'
    PASSWORD = 'iloveesd2020'

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart() # create a message

    message = "Dear {},\n\nYour appointment booking with Dr. Jackson Tan has been confirmed.\n\nTo attend your consultation, please login to the portal under the consultation tab.\n\nThank you!\n\nBest regards,\nO-HCare".format(patient_name)


    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']= patient_email
    msg['Subject']= "Appointment booking Confirmation"
    print(msg)
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    # send the message via the server set up earlier.
    s.send_message(msg)
    del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()

def receivePatient():
    channelqueue = channel.queue_declare(queue="notification", durable=True)
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='notification.patient') # bind the queue to the exchange via the key

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def callback(channel, method, properties, body):
    result = json.loads(body)
    print(result) # {'patientID':1, 'patient_name': 'Anne', ...}
    process_message(result)
    print(result)
    

def process_message(patient):
    patient_name = patient["patient_name"]
    patient_email = patient["patient_email"]
    send_email(patient_name, patient_email)
    print ("Email has been sent to the patient- {}".format(patient_name))
    return

if __name__ == "__main__":
    print("Receiving patient details...")
    receivePatient()
    app.run(debug=True)

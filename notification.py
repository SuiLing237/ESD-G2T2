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


hostname = "localhost" # default hostname
port = 5672 # default port
# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
    # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
    # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
channel = connection.channel()
# set up the exchange if the exchange doesn't exist
exchangename="patient_direct"
channel.exchange_declare(exchange=exchangename, exchange_type='direct')

# @app.route("/")
# def receive_booking_info():
#     patient = {
#     "patient_name" : "Anne",
#     "patient_phone" : "12348888",
#     "patient_email" : "Anne@hotmail.com"
#     "patient_password": "anne123"
# }



# can only send 10 text 
# def sendSMS(apikey, numbers, sender, message):
#     data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
#         'message' : message, 'sender': sender})
#     data = data.encode('utf-8')
#     request = urllib.request.Request("https://api.txtlocal.com/send/?")
#     f = urllib.request.urlopen(request, data)
#     fr = f.read()
#     return(fr)

# resp =  sendSMS('apikey', '	nOqbl/+J8Qk-QrHvwLDm4LvqZynSIL5OC2UeTx6PPv',
#     'Jims Autos', 'This is your message')
# print (resp)


# SL: I need retrieve patient from patient microservice and patient's booking details from doctor microservice via AMQP
# patient is in the form of a dictionary.
# def send_email_message(patient):
#     print("invoked")
#     patient_name = patient['patient_name']
#     patient_email = patient['patient_email'] # I tested using my own email, but doesn't work.
    
#     return requests.post(
# 		"https://api.mailgun.net/v3/sandbox8ced2597e4084a168f5ae34a977ca417.mailgun.org/messages",
# 		auth=("api", "2c0d1e53b653f0d410046ea5c476e6c7-9a235412-8ecb4f09"),
# 		data={"from": "Mailgun Sandbox <postmaster@sandbox8ced2597e4084a168f5ae34a977ca417.mailgun.org>",
#             #"to": "samuel low <samuel.low.2018@smu.edu.sg>",
#             "to": "{}<{}>".format(patient_name, patient_email),
# 			"subject": "Hello xxxx",
# 			#"text": "Dear Customer, your bill is here!  You are truly awesome!"
#             "text": "Dear {}, your booking of appointment with the doctor is confirmed. Here are your booking details {}".format(patient_name, booking_time)})
# print(send_email_message())




def send_email(patient_name, patient_email):
    MY_ADDRESS = 'sender emal'
    PASSWORD = 'sender pass'
    names = "sam"
    emails = "mushi.lee.2018@smu.edu.sg"

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    msg = MIMEMultipart()       # create a message

    message = "Dear {},\n   Your appointment booking with Dr.Jackson has been confirmed. Please login into the portal for the consultation. Thank you".format(patient_name)


    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']= patient_email
    msg['Subject']= "Appointment booking Confirmation"
    print(msg)
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))

    send the message via the server set up earlier.
    s.send_message(msg)
    del msg
        
    Terminate the SMTP session and close the connection
    s.quit()


def receivePatient():
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="notification", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='notification.patient') # bind the queue to the exchange via the key

    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True) # 'auto_ack=True' acknowledges the reception of a message to the broker automatically, so that the broker can assume the message is received and processed and remove it from the queue
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

# I wonder how the result will look like if notif microservice also receives doctor
def callback(channel, method, properties, body): # required signature for the callback; no return
    result = json.loads(body)
    # print(type(result)) # dict
    # print(result) # {'patientID':1, 'patient_name': 'Anne', ...}
    # send_email_message(result)
    process_message(result)
    print(result)
    

def process_message(patient):
        patient_name = patient["patient_name"]
        patient_email = patient["patient_email"]
        send_email(patient_name,patient_email)
        print ("Email has been sent to the patient- {}".format(patient_name))
        return

if __name__ == "__main__":
    print("Receiving patient details...")
    receivePatient()
    # main()
    app.run(debug=True)

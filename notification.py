import requests
import urllib.request
import urllib.parse
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient' # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

@app.route("/")
def receive_booking_info():
    booking_info = {
    "patient_name" : "mushi",
    "patient_email" : "mushi.lee.2018@smu.edu.sg",
    "booking_time" : "10"
}
    patient_name = booking_info["patient_name"]
    patient_email = booking_info["patient_email"]
    booking_time = booking_info["booking_time"]
    send_email_message(patient_name,patient_email,booking_time)
    return "done"


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


# SL: I need retrieve patient_email from patient microservice via AMQP, someone help :')
@app.route("/notification/send_booking_confirmation_email/<string:patient_email>/")
def send_email_message(patientID):
	return requests.post(
		"https://api.mailgun.net/v3/sandbox8ced2597e4084a168f5ae34a977ca417.mailgun.org/messages",
		auth=("api", "2c0d1e53b653f0d410046ea5c476e6c7-9a235412-8ecb4f09"),
		data={"from": "Mailgun Sandbox <postmaster@sandbox8ced2597e4084a168f5ae34a977ca417.mailgun.org>",
			#"to": "samuel low <samuel.low.2018@smu.edu.sg>",
            "to": "{}<{}>".format(patient_name, patient_email),
			"subject": "Hello xxxx",
			#"text": "Dear Customer, your bill is here!  You are truly awesome!"
            "text": "Dear {}, your booking of appointment with the doctor is confirmed. Here are your booking details {}".format(patient_name, booking_time)})
# print(send_email_message())


if __name__ == "__main__":
    app.run(debug=True)
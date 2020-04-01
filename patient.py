from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import json
import pika # for amqp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient' # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Patient(db.Model):
    __tablename__ = "patient"

    patientID = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(64), nullable=False)
    patient_phone = db.Column(db.Integer, nullable=False)
    patient_email = db.Column(db.String(64), nullable=False)
    patient_password = db.Column(db.String(64),nullable=False)

    def __init__(self, patientID, patient_name, patient_phone, patient_email, patient_password):
        self.patientID = patientID
        self.patient_name = patient_name
        self.patient_phone = patient_phone
        self.patient_email = patient_email
        self.patient_password = patient_password
    
    def json(self):
        return {"patientID": self.patientID, "patient_name": self.patient_name, "patient_phone": self.patient_phone, 'patient_email': self.patient_email, "patient_password": self.patient_password}

@app.route("/")
def home():
    return "Your application is working!"

@app.route("/patient/")
def get_all_patients():
    return jsonify({"patients": [patient.json() for patient in Patient.query.all()]})

@app.route("/patient/<int:patientID>/")
def get_patient(patientID):
    patient = Patient.query.filter_by(patientID=patientID).first()
    if patient:
        return jsonify(patient.json())
    return jsonify({"message": "Patient does not exist."}), 404


@app.route("/patient/", methods=["POST"])
def create_patient():
    last_id = Patient.query.order_by(Patient.patientID.desc()).first()
    if last_id:
        new_id = last_id.patientID
        new_id += 1

    data = request.get_json()
    patient = Patient(new_id, **data)

    try:
        db.session.add(patient)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the patient."}), 500

    return jsonify(patient.json()), 201

    #session.query(ObjectRes).order_by(ObjectRes.id.desc()).first()
# @app.route("/patient/<int:patientID>/", methods=["POST"])
# def create_patient(patientID):
#     if (Patient.query.filter_by(patientID=patientID).first()):
#         return jsonify({"message": "A patient with patientID '{}' already exists.".format(patientID)}), 400  
#     data = request.get_json()
#     patient = Patient(patientID, **data)

#     try:
#         db.session.add(patient)
#         db.session.commit()
#     except:
#         return jsonify({"message": "An error occurred creating the patient."}), 500

#     return jsonify(patient.json()), 201

@app.route("/patient/<string:patient_email>/<string:patient_password>/")
def verify_and_retrieve_patient(patient_email, patient_password):
    if (patient_email == "Missing" or patient_password == "Missing"):
        return jsonify({"message": "Missing inputs."}), 400

    # check if email exists
    if (Patient.query.filter_by(patient_email=patient_email).first()):
        # check if password matches
        if (Patient.query.filter_by(patient_password=patient_password).first()):
            # retrieve patientID
            patient = Patient.query.filter_by(patient_email=patient_email, patient_password=patient_password).first()
            return jsonify(patient.json()), 201
        else:
            return jsonify({"message": "Password does not match email address."}), 400
    else:
        return jsonify({"message": "A patient with that email address '{}' does not exist.".format(patient_email)}), 400

# sends patient to notification microservice via direct AMQP
@app.route("/send_patient/<int:patientID>/")
def start_send(patientID):
    send_patient(patientID)
    return "Start send, OK"

def send_patient(patientID):
    patient = Patient.query.filter_by(patientID=patientID).first()
    patientJSON = patient.json()
    # print(type(patient))
    # print(type(patientJSON))

    hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="patient_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare the message body content
    message = json.dumps(patientJSON, default=str) # convert a JSON object to a string

    # prepare the channel and send a message to Shipping
    channel.queue_declare(queue='notification', durable=True) # make sure the queue used by Shipping exist and durable
    channel.queue_bind(exchange=exchangename, queue='notification', routing_key='notification.patient') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="notification.patient", body=message,
        properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
        )
    )
    print("Patient sent to notification")
    # close the connection to the broker
    connection.close()

# IF DON'T NEED BELOW FUNCTIONS, I SHALL DELETE
# This is a helper function
# def calculate_medicine_cost(price, quantity):
#     cost = price * quantity
#     return cost

# # @app.route("/patient/<int:patientID>")
# def calculate_total_bill(patientID, prescription_dict):
#     # I will need the prescription_dict in order to continue.
#     pass

# some auto-increment code YN tried
# @app.route("/patient", methods=["POST"])
# def create_patient(): #auto-increment the ID
#     status = 201
#     #return jsonify({"message": "New patient created:"}), status  
    
#     data = request.get_json()
#     patient_name = request.json.get('patient_name', None)
#     patient = Patient(patient_name, **data)

#     if status == 201:
#         try:
#             db.session.add(patient)
#             db.session.commit()
#         except Exception as e:
#             return jsonify({"message": "An error occurred creating the patient."}), 500
    
#     return jsonify(patient.json()), 201


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
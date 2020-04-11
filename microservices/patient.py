from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# for amqp
import json
import pika

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

	def __init__(self, patientID, patient_email, patient_name, patient_phone,  patient_password):
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


@app.route("/patient/<string:patient_email>/", methods=["POST"])
def create_patient(patient_email):
    last_id = Patient.query.order_by(Patient.patientID.desc()).first()
    if last_id:
        new_id = last_id.patientID
        new_id += 1

    data = request.get_json()
    print(data)
    patient = Patient(new_id, patient_email, **data)

    try:
        db.session.add(patient)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the patient."}), 500

    return jsonify(patient.json()), 201

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
@app.route("/send_patient/<int:patientID>/", methods=['POST'])
def start_send(patientID):
	send_patient(patientID)
	return "Start send, OK"

def send_patient(patientID):
	patient = Patient.query.filter_by(patientID=patientID).first()
	patientJSON = patient.json()

	hostname = "localhost"
	port = 5672

	connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
	channel = connection.channel()

	exchangename="patient_direct"
	channel.exchange_declare(exchange=exchangename, exchange_type='direct')

	message = json.dumps(patientJSON, default=str)

	channel.queue_declare(queue='notification', durable=True)
	channel.queue_bind(exchange=exchangename, queue='notification', routing_key='notification.patient')
	channel.basic_publish(exchange=exchangename, routing_key="notification.patient", body=message,
		properties=pika.BasicProperties(delivery_mode = 2)
	)
	print("Patient sent to notification")
	connection.close()


if __name__ == "__main__":
	app.run(port=5001, debug=True)

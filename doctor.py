from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# for amqp
import json
import pika

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/doctor' # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Doctor(db.Model):
    __tablename__ = 'doctor'

    # We only have 1 doctor
    bookingID = db.Column(db.Integer, primary_key=True)
    patientID = db.Column(db.Integer) # added so can view bookings by patientID
    date = db.Column(db.String(64), nullable=False)
    timeslot = db.Column(db.String(64), nullable = False)
    availability = db.Column(db.String(64), nullable=False)

    # Ideal way to store the schedule/ availability of the doctor?

    def __init__(self, bookingID, patientID, date, timeslot, availability): # initialise book objects
        self.bookingID = bookingID
        self.patientID = patientID
        self.date = date
        self.timeslot = timeslot
        self.availability = availability

    def json(self):
        return {"bookingID":self.bookingID, "patientID":self.patientID, "date":self.date, "timeslot": self.timeslot, "availability": self.availability}

class DoctorInfo(db.Model):
    __tablename__ = 'doctor_info'

    # We only have 1 doctor
    doctorID = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(64), nullable=False) # added so can view bookings by patientID
    doctor_email = db.Column(db.String(64), nullable=False)
    doctor_password = db.Column(db.String(64), nullable = False)

    # Ideal way to store the schedule/ availability of the doctor?

    def __init__(self, doctorID, doctor_name, doctor_email, doctor_password): # initialise book objects
        self.doctorID = doctorID
        self.doctor_name = doctor_name
        self.doctor_email = doctor_email
        self.doctor_password = doctor_password

    def json(self):
        return {"doctorID":self.doctorID, "doctor_name":self.doctor_name, "doctor_email":self.doctor_email, "doctor_password": self.doctor_password}

@app.route("/")
def home():
    return "Your application is working!"

@app.route("/doctor/")
def get_all_details(): # Can retrieve Availability
    return jsonify({"doctor details": [doctor.json() for doctor in Doctor.query.all()]})

# -- Did not include function for Doctor not found since we only have 1 doctor now. But we can change further if needed. 

@app.route("/getAllPatientBookings/<string:date>/")
def get_patient_bookings(date):
    doctor = Doctor.query.filter_by(date=date, availability="NO")
    if doctor:
        return jsonify({"availability": [avail.json() for avail in doctor]})

# retrieve by specific date
@app.route("/doctor/<string:date>/")
def get_availability_by_date(date):
    doctor = Doctor.query.filter_by(date=date, availability="YES")
    if doctor:
        return jsonify({"availability": [avail.json() for avail in doctor]})

# update doctor availability with bookingID and patientID
@app.route("/doctor/<int:bookingID>/<int:patientID>/", methods=["PUT"])
def update_doctor_availability(bookingID, patientID):
    # query if timing is already booked
    # -----
    # doctor = Doctor.query.filter_by(date=date, time=time).first()
    doctor = Doctor.query.filter_by(bookingID=bookingID).first()
    if doctor:
        if(doctor.availability == 'YES'):
            try:
                doctor.availability = 'NO'
                doctor.patientID = patientID
                db.session.commit()

                return jsonify({"message": "Booking ID {} successfully made.".format(bookingID)}), 201 

            except Exception as e:
                # return jsonify({"message": "Booking ID {} is not available.".format(bookingID)}), 401
                return (str(e))

        return jsonify({"message": "Booking ID {} is not available.".format(bookingID)}), 401

    #     return "This timeslot is not available", 400
    # return "This date and timeslot is not available", 400
    else:
        return jsonify({"message": "The booking ID {} does not exists.".format(bookingID)}), 400  

# retrieve bookings by patientID
@app.route("/doctor/<int:patientID>/")
def get_bookings_by_patientID(patientID):
    doctor = Doctor.query.filter_by(patientID=patientID, availability="NO")
    if doctor:
        return jsonify({"availability": [avail.json() for avail in doctor]})

# retrieve booking by bookingID
@app.route("/booking/<int:bookingID>/")
def get_booking_by_bookingID(bookingID):
    doctor = Doctor.query.filter_by(bookingID=bookingID)
    if doctor:
        return jsonify({"booking": booking.json() for booking in doctor})


@app.route("/doctor/<string:doctor_email>/<string:doctor_password>/")
def verify_and_retrieve_doctor(doctor_email, doctor_password):
	if (doctor_email == "Missing" or doctor_password == "Missing"):
		return jsonify({"message": "Missing inputs."}), 400

	# check if email exists
	if (DoctorInfo.query.filter_by(doctor_email=doctor_email).first()):
		# check if password matches
		if (DoctorInfo.query.filter_by(doctor_password=doctor_password).first()):
			# retrieve patientID
			doctor = DoctorInfo.query.filter_by(doctor_email=doctor_email, doctor_password=doctor_password).first()
			return jsonify(doctor.json()), 201
		else:
			return jsonify({"message": "Password does not match email address."}), 400
	else:
		return jsonify({"message": "A doctor with that email address '{}' does not exist.".format(doctor_email)}), 400



# KIV AMQP
# # sends booking slot to notification microservice via direct AMQP
# @app.route("/send_booking/<int:bookingID>/")
# def start_send(bookingID):
#     send_booking(bookingID)
#     return "Start send, OK"

# def send_booking(bookingID):
#     booking = Doctor.query.filter_by(bookingID=bookingID).first()
#     bookingJSON = booking.json()
#     # print(type(booking))
#     # print(type(bookingJSON))

#     hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
#     port = 5672 # default messaging port.
#     # connect to the broker and set up a communication channel in the connection
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
#         # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
#         # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
#     channel = connection.channel()

#     # set up the exchange if the exchange doesn't exist
#     exchangename="booking_direct"
#     channel.exchange_declare(exchange=exchangename, exchange_type='direct')

#     # prepare the message body content
#     message = json.dumps(bookingJSON, default=str) # convert a JSON object to a string

#     # prepare the channel and send a message to Shipping
#     channel.queue_declare(queue='notification', durable=True) # make sure the queue used by Shipping exist and durable
#     channel.queue_bind(exchange=exchangename, queue='notification', routing_key='notification.booking') # make sure the queue is bound to the exchange
#     channel.basic_publish(exchange=exchangename, routing_key="notification.booking", body=message,
#         properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
#         )
#     )
#     print("Booking sent to notification")
#     # close the connection to the broker
#     connection.close()

if __name__ == "__main__":
    app.run(port=5007, debug=True)
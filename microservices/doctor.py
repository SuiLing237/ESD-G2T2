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

    bookingID = db.Column(db.Integer, primary_key=True)
    patientID = db.Column(db.Integer)
    date = db.Column(db.String(64), nullable=False)
    timeslot = db.Column(db.String(64), nullable = False)
    availability = db.Column(db.String(64), nullable=False)

    def __init__(self, bookingID, patientID, date, timeslot, availability):
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
    doctor_name = db.Column(db.String(64), nullable=False)
    doctor_email = db.Column(db.String(64), nullable=False)
    doctor_password = db.Column(db.String(64), nullable = False)

    def __init__(self, doctorID, doctor_name, doctor_email, doctor_password):
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
def get_all_bookings(): # Can retrieve Availability
    return jsonify({"doctor details": [doctor.json() for doctor in Doctor.query.all()]})

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
    doctor = Doctor.query.filter_by(bookingID=bookingID).first()
    if doctor:
        if(doctor.availability == 'YES'):
            try:
                doctor.availability = 'NO'
                doctor.patientID = patientID
                db.session.commit()

                return jsonify({"message": "Booking ID {} successfully made.".format(bookingID)}), 201 
            except Exception as e:
                return (str(e))

        return jsonify({"message": "Booking ID {} is not available.".format(bookingID)}), 401
    else:
        return jsonify({"message": "The booking ID {} does not exists.".format(bookingID)}), 400  

# retrieve bookings by patientID
@app.route("/doctor/<int:patientID>/")
def get_bookings_by_patientID(patientID):
    doctor = Doctor.query.filter_by(patientID=patientID, availability="NO")
    if doctor:
        return jsonify({"availability": [avail.json() for avail in doctor]}), 200

# retrieve booking by bookingID
@app.route("/booking/<int:bookingID>/")
def get_booking_by_bookingID(bookingID):
    doctor = Doctor.query.filter_by(bookingID=bookingID)
    if doctor:
        return jsonify({"booking": booking.json() for booking in doctor}), 200


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

if __name__ == "__main__":
    app.run(port=5007, debug=True)
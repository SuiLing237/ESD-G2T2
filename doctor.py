from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

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

@app.route("/")
def home():
    return "Your application is working!"

@app.route("/doctor")
def get_all_details(): # Can retrieve Availability
    return jsonify({"doctor details": [doctor.json() for doctor in Doctor.query.all()]})

# -- Did not include function for Doctor not found since we only have 1 doctor now. But we can change further if needed. 

@app.route("/getAllPatientBookings/<string:date>/")
def get_patient_bookings(date):
    doctor = Doctor.query.filter_by(date=date, availability="NO")
    if doctor:
        return jsonify({"availability": [avail.json() for avail in doctor]})

# Query by specific date
@app.route("/doctor/<string:date>/")
def get_availability_by_date(date):
    doctor = Doctor.query.filter_by(date=date, availability="YES")
    if doctor:
        return jsonify({"availability": [avail.json() for avail in doctor]})

@app.route("/doctor/<int:bookingID>/", methods=["PUT"])
def update_doctor_availability(bookingID):
    # query if timing is already booked
    # -----
    # doctor = Doctor.query.filter_by(date=date, time=time).first()
    doctor = Doctor.query.filter_by(bookingID=bookingID).first()
    if doctor:
        if(doctor.availability == 'YES'):
            try:
                doctor.availability = 'N0'
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
def get_bookings_by_patientID(patienID):
    doctor = Doctor.query.filter_by(patientID=patientID)
    if doctor:
        return jsonify({"doctor availability": [avail.json() for avail in doctor]})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
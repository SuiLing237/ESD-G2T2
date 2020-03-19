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
    date = db.Column(db.String(64), nullable=False)
    timeslot = db.Column(db.String(64), nullable = False)
    availability = db.Column(db.String(64), nullable=False)

    # Ideal way to store the schedule/ availability of the doctor?

    def __init__(self, bookingID, date, timeslot, availability): # initialise book objects
        self.bookingID = bookingID
        self.date = date
        self.timeslot = timeslot
        self.availability = availability

    def json(self):
        return {"bookingID":self.bookingID, "date":self.date, "timeslot": self.timeslot, "availability": self.availability}


@app.route("/doctor")
def get_all_details(): # Can retrieve Availability
    return jsonify({"doctor details": [doctor.json() for doctor in Doctor.query.all()]})

# -- Did not include function for Doctor not found since we only have 1 doctor now. But we can change further if needed. 

@app.route("/doctor/<string:date>/") # Query by specific date
def get_availability_by_date(date):
    doctor = Doctor.query.filter_by(date=date)
    if doctor:
        return jsonify(doctor.json())
    return "Doctor is not available on this date"   

@app.route("/doctor/<string:date>/<string:time>/<string:availability>/", methods=["POST"])
def book_consultation(date, time, availability):
    # query if timing is already booked
    # -----
    doctor = Doctor.query.filter_by(date=date, time=time).first()
    if doctor:
        if (doctor.columns.availability == None): # double check .columns.
            data = request.get_json()
            # doctor = Doctor()

            try:
                pass
            except:
                pass

            return jsonify(201)
            
        return "This timeslot is not available", 400
    return "This date and timeslot is not available", 400

# should we include Patient's ID in our app.route? 

if __name__ == "__main__":
    app.run(debug=True)
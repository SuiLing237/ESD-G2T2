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
    ID = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(64), nullable = False)
    address = db.Column(db.String(100), nullable= False)
    phone = db.Column(db.Integer, nullable = False) # PS, do we really need to store the phone number?
    availability = db.String(db.String)
    # Ideal way to store the schedule/ availability of the doctor?

    def __init__(self, name, address, phone, availability): # initialise book objects
        self.name = name
        self.address = address
        self.phone = phone
        self.availability = availability

    def json(self):
        return {"name": self.name, "address": self.address, "phone": self.phone, "availability": self.availability}


@app.route("/doctor")
def get_all_details(): # Can retrieve Availability
    return jsonify({"doctor details": [doctor.json() for doctor in Doctor.query.all()]})

# -- Did not include function for Doctor not found since we only have 1 doctor now. But we can change further if needed. 

@app.route("/doctor/<string:availability>", methods=["POST"])
def book_consultation(availability):
    # query if timing is already booked
    # -----

    data = request.get_json()

    try:
        pass
    except:
        pass
    return jsonify(201)

# should we include Patient's ID in our app.route? 



if __name__ == "__main__":
    app.run(debug=True)
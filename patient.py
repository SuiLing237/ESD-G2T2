from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient' # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# SL: Since we have 3 tables in Patient DB now, how do I list the 2 tables `prescription` and `diagnosis` here?
class Patient(db.Model):
    __tablename__ = "patient"

    patientID = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(64), nullable=False)
    patient_phone = db.Column(db.Integer, nullable=False)

    def __init__(self, patientID, patient_name, patient_phone):
        self.patientID = patientID
        self.patient_name = patient_name
        self.patient_phone = patient_phone
    
    def json(self):
        return {"patientID": self.patientID, "patient_name": self.patient_name, "patient_phone": self.patient_phone}

class Prescription(db.Model):
    __tablename__ = "prescription"

    patientID = db.Column(db.Integer, primary_key=True)
    bookingID = db.Column(db.Integer, nullable=False)
    medicineID = db.Column(db.Integer, foreign_key=True, nullable=False)
    medicine_quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, patientID, bookingID, medicineID, medicine_quantity):
        self.patientID = patientID
        self.bookingID = bookingID
        self.medicineID = medicineID
        self.medicine_quantity = medicine_quantity
    
    def json(self):
        return {"patientID": self.patientID, "bookingID": self.bookingID, "medicineID": self.medicineID, "medicine_quantity": self.medicine_quantity}

class Diagnosis(db.Model):
    __tablename__ = "diagnosis"

    patientID = db.Column(db.Integer, primary_key=True)
    bookingID = db.Column(db.Integer, nullable=False)
    diagnosis = db.Column(db.String(64), nullable=False)
    
    def __init__(self, patientID, bookingID, diagnosis):
        self.patientID = patientID
        self.bookingID = bookingID
        self.diagnosis = diagnosis
    
    def json(self):
        return {"patientID": self.patientID, "bookingID": self.bookingID, "diagnosis": self.diagnosis}

@app.route("/")
def home():
    return "Your application is working!"

@app.route("/patient")
def get_all_patients():
    return jsonify({"patients": [patient.json() for patient in Patient.query.all()]})

@app.route("/patient/<int:patientID>")
def get_patient(patientID):
    patient = Patient.query.filter_by(patientID=patientID).first()
    if patient:
        return jsonify(patient.json())
    return jsonify({"message": "Patient does not exist."}), 404

@app.route("/patient/<int:patientID>", methods=["POST"])
def create_patient(patientID):
    if (Patient.query.filter_by(patientID=patientID).first()):
        return jsonify({"message": "A patient with patientID '{}' already exists.".format(patientID)}), 400  
    data = request.get_json()
    patient = Patient(patientID, **data)

    try:
        db.session.add(patient)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the patient."}), 500

    return jsonify(patient.json()), 201

# This is a helper function
def calculate_medicine_cost(price, quantity):
    cost = price * quantity
    return cost

@app.route("/patient/<int:patientID>")
def calculate_total_bill(patientID, prescription_dict):
    # I will need the prescription_dict in order to continue.
    pass


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
    app.run(debug=True)
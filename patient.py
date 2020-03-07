from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/patient' # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Patient(db.Model):
    __tablename__ = "patient"

    patientID = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    prescription = db.Column(db.String(64))

    def __init__(self, patientID, patient_name, address, phone, prescription):
        self.patientID = patientID
        self.patient_name = patient_name
        self.address = address
        self.phone = phone
        self.prescription = prescription
    
    def json(self):
        return {"patientID": self.patientID, "patient_name": self.patient_name, "address": self.address, "phone": self.phone, "prescription": self.prescription}


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


@app.route("/patient/<int:patientID>/<int:bookingID>", methods=["POST"])
def create_booking(bookingID):
    pass

if __name__ == "__main__":
    app.run(debug=True)
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

@app.route("/patient")
def get_all_patients():
    return jsonify({"patients": [patient.json() for patient in Patient.query.all()]})

@app.route("/patient/<int:patientID>")
def get_patient(patientID):
    patient = Patient.query.filter_by(patientID=patientID).first()
    if patient:
        return jsonify(patient.json())
    return jsonify({"message": "Patient does not exist."}), 404

@app.route("/patient/<int:patientID>/", methods=["POST"])
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
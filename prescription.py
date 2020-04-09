from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/prescription' # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

pricelistURL = "http://localhost:5006/price"

class Prescription(db.Model):
    __tablename__ = "prescription"


    itemID = db.Column(db.Integer, primary_key=True)
    patientID = db.Column(db.Integer, nullable=False)
    bookingID = db.Column(db.Integer, nullable=False)
    medicineID = db.Column(db.Integer, nullable=False)
    medicine_quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, itemID, patientID, bookingID, medicineID, medicine_quantity):
        self.itemID = itemID
        self.patientID = patientID
        self.bookingID = bookingID
        self.medicineID = medicineID
        self.medicine_quantity = medicine_quantity
    
    def json(self):
        return {"patientID": self.patientID, "bookingID": self.bookingID, "medicineID": self.medicineID, "medicine_quantity": self.medicine_quantity}

@app.route("/")
def home():
    return "Your application is working!"

@app.route("/createPrescription/<int:patientID>/<int:bookingID>/", methods=['POST'])
def create_new_prescription(patientID, bookingID):
    last_id = Prescription.query.order_by(Prescription.itemID.desc()).first()
    if last_id:
        new_id = last_id.itemID
        new_id += 1
    else:
        new_id = 1
    
    data = request.get_json()

    d = Prescription(new_id, patientID, bookingID, **data)

    try:
        db.session.add(d)
        db.session.commit()
    
    except:
        return jsonify({"message": "An error occurred while creating prescription."}), 500

    return jsonify({"message":"Prescription added successfully!"}), 200


# SL: Mushi, can delete?
@app.route("/prescription/", methods=["POST"])
def create_prescription(prescription):
 # status in 2xx indicates success
    status = 201
    result = {}

    # retrieve information about order and order items from the request
    patient_id = request.json.get('patient_id', None)
    order = Order(patient_id = patient_id)
    prescription = request.json.get('prescription')
    for index, ci in enumerate(prescription):
        pass
    #     if 'med_id' in prescription[index] and 'quantity' in prescription[index]:
    #         order.order_item.append(Order_Item(med_id = prescription[index]['med_id'], quantity = prescription[index]['quantity']))
    #     else:
    #         status = 400
    #         result = {"status": status, "message": "Invalid 'med_id' or 'quantity'."}
    #         break

    # if status==201 and len(order.order_item)<1:
    #     status = 404
    #     result = {"status": status, "message": "Empty order."}

    # if status==201:
    #     try:
    #         db.session.add(order)
    #         db.session.commit()
    #     except Exception as e:
    #         status = 500
    #         result = {"status": status, "message": "An error occurred when creating the order in DB.", "error": str(e)}
        
    #     if status==201:
    #         result = order.json()

    # # FIXME: add a call to "send_order" copied from another appropriate file
    # send_order(result)
    # return str(result), status
    return

@app.route("/<int:patientID>/<int:bookingID>")
def view_prescription(patientID, bookingID):
    result = retrieve_prescription(patientID, bookingID)
    return (result)

@app.route("/retrieve/<int:patientID>/<int:bookingID>")
def retrieve_prescription(patientID, bookingID):
    patient_prescription = Prescription.query.filter_by(patientID=patientID, bookingID=bookingID).all() #assume that each patient has only one prescription in databse
    if patient_prescription:
        print(patient_prescription)
        start_send_prescription(patientID, bookingID)
        return {'prescription': [prescription.json() for prescription in patient_prescription]}
        # return jsonify(prescription.json())
    return jsonify({"message": "Prescription does not exist."}), 404

# This is a function to trigger send_prescription
# @app.route("/send/<int:patientID>/<int:bookingID>")
def start_send_prescription(patientID, bookingID):
    patient_prescription = Prescription.query.filter_by(patientID=patientID, bookingID=bookingID).all()
    message ={'patientID':patientID,'bookingID':bookingID,'prescription': [prescription.json() for prescription in patient_prescription]}

    #send to medicine microservice
    r = requests.post(pricelistURL, json = message)
    return "ok"
    print("Price sent to paypal.")

if __name__ == "__main__":
    app.run(port=5005, debug=True)
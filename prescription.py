from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/prescription' # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

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

@app.route("/")
def home():
    return "Your application is working!"

if __name__ == "__main__":
    app.run(debug=True)
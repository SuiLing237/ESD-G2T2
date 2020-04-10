from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

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

@app.route("/diagnosis/<int:patientID>/<int:bookingID>/", methods=['POST'])
def create_diagnosis(patientID, bookingID):
    if (Diagnosis.query.filter_by(patientID=patientID, bookingID=bookingID).first()): 
        return jsonify({"message": "A diagnosis with patientID '{}' and bookingID '{}' already exists.".format(patientID, bookingID)}), 400

    data = request.get_json()
    d = Diagnosis(patientID, bookingID, **data)
    print(data)
    print(d.json())

    try:
        db.session.add(d)
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred creating the book."}), 500
    
    return jsonify({"message": "Diagnosis added successfully!"}), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5002, debug=True)
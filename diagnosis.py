from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/diagnosis' # ENTER DB NAME HERE
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

if __name__ == "__main__":
    app.run(debug=True)
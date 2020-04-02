from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from sqlalchemy.exc import SQLAlchemyError

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

@app.route("/diagnosis/<int:patientID>/<int:bookingID>/", methods=['POST'])
def create_diagnosis(patientID, bookingID):
    if (Diagnosis.query.filter_by(patientID=patientID, bookingID=bookingID).first()): 
        return jsonify({"message": "A diagnosis with patientID '{}' and bookingID '{}' already exists.".format(patientID, bookingID)}), 400

    data = request.get_json() # <- POSTMAN. get request from POSTMAN
    d = Diagnosis(patientID, bookingID, **data) # **data is to get all the fields (e.g. availability, etc)
    print(data)
    print(d.json())

    try:
        db.session.add(d) # add the book to Database
        db.session.commit() 
    # except SQLAlchemyError as e:
    #     error = str(e.__dict__['orig'];
    #     return 'error'
    #     # return jsonify({"message": "An error occurred creating the diagnosis record."}), 500 # ERRROR MSG

    except:
        return jsonify({"message": "An error occurred creating the book."}), 500

    return jsonify(d.json()), 201 # if successful, return representation. 201 -> create. 500 for error. 

if __name__ == "__main__":
    app.run(port=5002, debug=True)
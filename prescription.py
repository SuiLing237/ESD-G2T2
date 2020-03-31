from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/prescription' # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

pricelistURL = "http://localhost:5000/price"

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


# This is a function to trigger send_prescriptionn
@app.route("/prescription/send")
def start_send_prescription():
    messege = json.dumps(medicineID, medicine_quantity, default=str) # convert a JSON object to a string

    #send to medicine microservice
    r = requests.post(pricelistURL, json = messege)
    print("Price sent to paypal.")

# # AMQP Function for sending Prescription
# def send_prescription(medicineID, medicine_quantity):
#     hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
#     port = 5672 # default messaging port.
#     # connect to the broker and set up a communication channel in the connection
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
#         # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
#         # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
#     channel = connection.channel()

#     # set up the exchange if the exchange doesn't exist
#     exchangename="prescription_direct"
#     channel.exchange_declare(exchange=exchangename, exchange_type='direct')

#     # prepare the message body content
#     message = json.dumps(medicineID, medicine_quantity, default=str) # convert a JSON object to a string

#     # prepare the channel and send a message to price_list
#     channel.queue_declare(queue='price_list', durable=True) # make sure the queue used by Shipping exist and durable
#     channel.queue_bind(exchange=exchangename, queue='price_list', routing_key='*.order') # make sure the queue is bound to the exchange
#     channel.basic_publish(exchange=exchangename, routing_key="prescription.price_list", body=message,
#         properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
#         )
#     )
#     print("Prescription details sent to price_list.")
#     # close the connection to the broker
#     connection.close()

if __name__ == "__main__":
    app.run(debug=True)
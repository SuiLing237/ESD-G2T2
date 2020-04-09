from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import paypalrestsdk
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/payment' # ENTER DB NAME HERE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Payment(db.Model):
    __tablename__ = "payment"

    patientID = db.Column(db.Integer, primary_key=True)
    bookingID = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    
    def __init__(self, patientID, bookingID, total_price):
        self.patientID = patientID
        self.bookingID = bookingID
        self.total_price = total_price
    
    def json(self):
        return {"patientID": self.patientID, "bookingID": self.bookingID, "total_price": self.total_price}


paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AT_uRRX_jQsZVKZXU-iMHj5qIcIfpc7aLh8kKgljsLcSJWcHmA030sBhcpwtI9LqVzszFX9aZJ0TjtVl",
  "client_secret": "EP1fgGYD5F73c5IlleCA7nVg6ivbeIIwPVYDbUdT5wK1CUyJus6gtkGAsgyHVizifJL_ufsVVKpkz-3L" })

@app.route('/')
def index():
    return render_template('billing.html')

@app.route('/create_payment/<int:patientID>/<int:bookingID>', methods=['POST'])
def create_payment(patientID, bookingID):
    if (Payment.query.filter_by(patientID=patientID, bookingID=bookingID).first()): 
        return jsonify({"message": "A record with patientID '{}' and bookingID '{}' already exists.".format(patientID, bookingID)}), 400

    data = request.get_json()
    d = Payment(patientID, bookingID, **data)
    print(data)
    print(d.json())

    try:
        db.session.add(d) # add the book to Database
        db.session.commit() 
    except:
        return jsonify({"message": "An error occurred creating the book."}), 500

    return jsonify(d.json()), 201

@app.route('/retrieve_price/<int:patientID>/<int:bookingID>')
def retrieve_price(patientID, bookingID):
    details= Payment.query.filter_by(patientID=patientID, bookingID=bookingID).first()
    if details:
        payment = details.json()
        return payment
    return jsonify({"message": "Book not found."}), 404

@app.route('/payment/<int:patientID>/<int:bookingID>', methods =['POST'])
def process_payment(patientID, bookingID):
    details= Payment.query.filter_by(patientID=patientID, bookingID=bookingID).first()
    if details:
        payment_amount = details.total_price
        print(payment_amount)
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:3000/payment/execute",
                "cancel_url": "http://localhost:3000/"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Medical Bill",
                        "sku": "12345",
                        "price": payment_amount,
                        "currency": "SGD",
                        "quantity": 1}]},
                "amount": {
                    "total": payment_amount,
                    "currency": "SGD"},
                "description": "Medical prescription bill."}]})

        if payment.create():
            print('Payment created!')
        else:
            print(payment.error)

        return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})

if __name__ == '__main__':
    app.run(port=5003, debug=True)
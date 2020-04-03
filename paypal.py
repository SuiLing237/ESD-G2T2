from flask import Flask, render_template, jsonify, request
import paypalrestsdk

app = Flask(__name__)

paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "AT_uRRX_jQsZVKZXU-iMHj5qIcIfpc7aLh8kKgljsLcSJWcHmA030sBhcpwtI9LqVzszFX9aZJ0TjtVl",
  "client_secret": "EP1fgGYD5F73c5IlleCA7nVg6ivbeIIwPVYDbUdT5wK1CUyJus6gtkGAsgyHVizifJL_ufsVVKpkz-3L" })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment', methods=['POST'])
def receive_payment():
    if request.is_json:
        payment = request.get_json()
        result = process_payment(payment)
        return result
    else:
        payment = request.get_data()
        print("Received invalid payment details:")
        print(payment)
        replymessage = json.dumps({"message": "Payment should be in JSON", "data": payment}, default=str)
        return replymessage, 400 # Bad Request

def process_payment(payment_amount):
    # print("payment")
    # print(type(payment))
    # return 

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
                    "name": "testitem",
                    "sku": "12345",
                    "price": payment_amount,
                    "currency": "SGD",
                    "quantity": 1}]},
            "amount": {
                "total": payment_amount,
                "currency": "SGD"},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
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
    app.run(debug=True)
import requests
import urllib.request
import urllib.parse


# can only send 10 text 
def sendSMS(apikey, numbers, sender, message):
    data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
        'message' : message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.txtlocal.com/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)

resp =  sendSMS('apikey', '	nOqbl/+J8Qk-QrHvwLDm4LvqZynSIL5OC2UeTx6PPv',
    'Jims Autos', 'This is your message')
print (resp)


def send_email_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandbox8ced2597e4084a168f5ae34a977ca417.mailgun.org/messages",
		auth=("api", "2c0d1e53b653f0d410046ea5c476e6c7-9a235412-8ecb4f09"),
		data={"from": "Mailgun Sandbox <postmaster@sandbox8ced2597e4084a168f5ae34a977ca417.mailgun.org>",
			"to": "samuel low <samuel.low.2018@smu.edu.sg>",
			"subject": "Hello xxxx",
			"text": "Dear Customer, your bill is here!  You are truly awesome!"})
print(send_email_message())
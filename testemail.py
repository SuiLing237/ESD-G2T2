# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail


# def send_email():
#     message = Mail(
#         from_email='dark_angel_0309@hotmail.com',
#         to_emails='samuel.low.2018@smu.edu.sg',
#         subject='Sending with Twilio SendGrid is Fun',
#         html_content='<strong>and easy to do anywhere, even with Python</strong>')
#     try:
#         sg = SendGridAPIClient(api_key='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')
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print(e.message)

# import smtplib

# sender = 'dark_angel_0309@hotmail.com'
# receivers = ['samuel.low.2018@smu.edu.sg']

# message = """From: From Person <dark_angel_0309@hotmail.com>
# To: To Person <samuel.low.2018@smu.edu.sg>
# Subject: SMTP e-mail test

# This is a test e-mail message.
# """

# try:
#    smtpObj = smtplib.SMTP('localhost')
#    smtpObj.sendmail(sender, receivers, message)         
#    print ("Successfully sent email")
# except smtplib.SMTPException:
#    print ("Error: unable to send email")

# import smtplib, ssl

# port = 587   # For SSL
# smtp_server = "smtp-mail.outlook.com"
# sender_email = "dark_angel_0309@hotmail.com"  # Enter your address
# receiver_email = "samuel.low.2018@smu.edu.sg"  # Enter receiver address
# password = input("Type your password and press enter: ")
# message = """\
# Subject: Hi there

# This message is sent from Python."""

# context = ssl.create_default_context()
# with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, message)



import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'dark_angel_0309@hotmail.com'
PASSWORD = ''

# def get_contacts(filename):
#     """
#     Return two lists names, emails containing names and email addresses
#     read from a file specified by filename.
#     """
    
#     names = []
#     emails = []
#     with open(filename, mode='r', encoding='utf-8') as contacts_file:
#         for a_contact in contacts_file:
#             names.append(a_contact.split()[0])
#             emails.append(a_contact.split()[1])
#     return names, emails

# def read_template(filename):
#     """
#     Returns a Template object comprising the contents of the 
#     file specified by filename.
#     """
    
#     with open(filename, 'r', encoding='utf-8') as template_file:
#         template_file_content = template_file.read()
#     return Template(template_file_content)

def main():
   names = "sam"
   emails = "mushi.lee.2018@smu.edu.sg"

   # set up the SMTP server
   s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
   s.starttls()
   s.login(MY_ADDRESS, PASSWORD)
   
   msg = MIMEMultipart()       # create a message

   # add in the actual person name to the message template
   message = "This is for  testing"


   # setup the parameters of the message
   msg['From']=MY_ADDRESS
   msg['To']=emails
   msg['Subject']="This is TEST"
   
   # add in the message body
   msg.attach(MIMEText(message, 'plain'))
   
   # send the message via the server set up earlier.
   s.send_message(msg)
   del msg
      
   # Terminate the SMTP session and close the connection
   s.quit()
    
if __name__ == '__main__':
    main()
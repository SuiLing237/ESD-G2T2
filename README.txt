IS213 ESD Project
Section: G2
Team: 2

Assumptions:
- Our data only has appointment slots from 13/4/20 to 17/4/20.
- "Go to consultation" button will only appear if your current system date corresponds to the appointment date.
- There is only one doctor.
- The patients only have max 1 appointment booked, can only book another after the current consultation ends and is paid for.

Instructions:
1) Place the code directly under your wamp/www/ for the links to work. #SL: Later we need to check that the redirection of links work
2) Make sure your WAMP is on.
3) Run all the sql files in phpmyadmin database.
4) Install paypal sdk using command prompt #SL: bernard what's the link
5) Change your laptop's system date to 13/4/20 or before as we only have timeslots data from 13/4/20 to 17/4/20.
6) Run all microservices:
- patient.py
- doctor.py
- prescription.py
- diagnosis.py
- notification.py
- price.py
- paypal.py (in ESD_API folder)

Flow of using the website:
1) Sign up as a patient with your real email (other particulars such as phone number can be fake).
2) Log in as a patient with your email and password.
3) Book an appointment.
4) Check that you received an email of successful booking confirmation.
5) Log out then log in as a doctor with these particulars:
- email: jacksontan@hotmail.com
- password: jackson123
- type: doctor
6) View your scheduled appointments.
7) Go to consultation.
8) Submit your diagnosis.
9) Click "Proceed to add prescription.".
10) Select type and quantity of medicine.
11) Log out then log in as the same patient again.
12) Go to payment.
13) Pay via paypal.
14) Logout of patient account.
# BBQ Guest List - QR Check-In Proof of Concept

## Project Overview
This project is a proof of concept for a QR-based guest check-in system using a Raspberry Pi.

The system allows a guest to register through a Flask web page, generates a QR code for that guest, and then uses the Raspberry Pi camera to scan the QR code.
The scanned code is validated against the guest list stored in a JSON file. 
The Sense HAT provides visual feedback:

- Green = valid guest checked in
- Red = invalid QR / duplicate entry / no QR detected

## Main Features
- Guest registration form using Flask
- Guest data stored in JSON
- QR code generation for each registered guest
- QR code scanning using Raspberry Pi camera
- Validation against stored guest records
- Sense HAT feedback for check-in result

## Technologies and Libraries Used
- Flask
- json
- os
- time
- datetime

### Raspberry Pi Hardware Libraries
- sense_hat
- picamera2

### Extra Libraries
- qrcode
- pyzbar
- Pillow

## Project Files
- app.py
  Runs the Flask registration app and generates QR codes for guests.

- qr_scanner.py
  Uses the Sense HAT button and Raspberry Pi camera to scan and validate QR codes.

- templates/index.html
  Registration page.

- templates/success.html
  Success page showing the generated QR code.

- state/guests.json
  Stores guest registration and check-in data.

- static/qrcodes/
  Stores generated QR code images.

- static/scan_test.jpg
  Temporary image captured by the Raspberry Pi camera during scanning.

## How the System Works
1. A guest opens the registration page hosted on the Raspberry Pi.
2. The guest enters their name and email.
3. The system stores the guest in guests.json.
4. A unique guest ID is generated.
5. A QR code is generated using that guest ID.
6. At check-in, the Raspberry Pi camera captures an image when the Sense HAT middle button is pressed.
7. The QR code is decoded from the captured image.
8. The decoded value is compared against the saved guest records.
9. The Sense HAT shows the result:
   - Green for valid first-time check-in
   - Red for invalid or duplicate entry

## How to Run

1. Open the project

cd ~/bbq-checkin
source .venv/bin/activate

2. Run the registration app

python app.py

Then open in a browser using your Raspberry Pi IP address, for example:

http://192.168.0.230:5000/

3. Run the QR scanner

Open another terminal and run:

cd ~/bbq-checkin
source .venv/bin/activate
python qr_scanner.py

## Check-In Flow
1. Register a guest on the Flask page
2. A QR code is generated
3. Show the QR code to the Raspberry Pi camera
4. Press the middle button on the Sense HAT
5. The system scans the QR and checks it against guests.json

## Output Meaning
- Green light: valid guest, checked in successfully
- Red light: invalid guest, duplicate entry, or no QR detected

## Example Guest Record
{
  "guest_id": "BBQ-0002",
  "name": "Barbara",
  "email": "barbara@gmail.com",
  "qr_value": "BBQ-0002",
  "qr_image": "qrcodes/BBQ-0002.png",
  "registered_at": "2026-05-09T13:20:03",
  "checked_in": true,
  "checked_in_at": "2026-05-11T17:47:59"
}


## Future Improvements
- Improve the user interface with CSS
- Add a guest list page in Flask
- Add Blynk integration as an extra feature

## Youtube link for video
- https://youtu.be/Zpw3UfWGBc4

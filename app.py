from flask import Flask, render_template, request   
import json                                         
import os                                           
from datetime import datetime                       
import qrcode                                       # library used to generate QR code images

app = Flask(__name__)                               # create the Flask web app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # get the folder where app. 0is stored
STATE_PATH = os.path.join(BASE_DIR, "state", "guests.json")  # Path to the JSON file storing guests
QR_DIR = os.path.join(BASE_DIR, "static", "qrcodes")         # Path to the folder where QR images will be saved

os.makedirs(QR_DIR, exist_ok=True)                  # create the QR folder if it does not already exist 

def load_guests():
    try:                                            # try to open and read the JSON file
        with open(STATE_PATH, "r") as f:            
            return json.load(f)                     
    except FileNotFoundError:                       # if the file does not exist yet
        return {"guests": []}                       # return an empty structure instead

def save_guests(data):
    with open(STATE_PATH, "w") as f:                # open json in write mode
        json.dump(data, f, indent=2)                # save Python data into JSON format

def generate_guest_id(data):
    next_number = len(data["guests"]) + 1           # count current guests and add 1 for the next ID
    return f"BBQ-{next_number:04d}"                 # create ID like BBQ-0001, BBQ-0002

def generate_qr_code(qr_value, guest_id):
    qr = qrcode.make(qr_value)                      # create a QR image from the value we want
    filename = f"{guest_id}.png"                    # make the QR image filename match the guest ID
    filepath = os.path.join(QR_DIR, filename)       # build full file path for the QR image
    qr.save(filepath)                               # save the QR image file
    return f"qrcodes/{filename}"                    # return the path used by Flask

@app.route("/")                                     
def home():
    return render_template("index.html")            # show the registration form page

@app.route("/register", methods=["POST"])           
def register():
    name = request.form.get("name")                 # read the name entered in the form
    email = request.form.get("email")               # read the email entered in the form

    data = load_guests()                            

    guest_id = generate_guest_id(data)              # generate a new unique guest ID
    qr_value = guest_id                             
    qr_image = generate_qr_code(qr_value, guest_id) # generate the QR image and get its saved

    new_guest = {                                   # create a new guest record
        "guest_id": guest_id,                       
        "name": name,                               
        "email": email,                             
        "qr_value": qr_value,                       
        "qr_image": qr_image,                       
        "registered_at": datetime.now().isoformat(timespec="seconds"),  
        "checked_in": False,                        
        "checked_in_at": None                       
    }

    data["guests"].append(new_guest)                # add this new guest to the guest list
    save_guests(data)                               

    return render_template("success.html", guest=new_guest)  # show success page and pass guest data to it

if __name__ == "__main__":                          
    app.run(host="0.0.0.0", port=5000, debug=True) 
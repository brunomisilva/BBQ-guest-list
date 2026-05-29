#!/usr/bin/env python3                             

import json                                         
import os                                            
import time                                          
from datetime import datetime                        

from sense_hat import SenseHat                       
from picamera2 import Picamera2                      
from pyzbar.pyzbar import decode                     # reads QR codes from an image
from PIL import Image                                # opens the saved image file for decoding

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))         
GUESTS_PATH = os.path.join(BASE_DIR, "state", "guests.json") 
IMAGE_PATH = os.path.join(BASE_DIR, "static", "scan_test.jpg")

# Sense hat and camera set up
sense = SenseHat()                                  
sense.clear()                                       

picam2 = Picamera2()                                
picam2.configure(picam2.create_still_configuration()) 
picam2.start()                                       
time.sleep(2)                                        

print("Camera ready. Press the Sense HAT middle button to scan a QR code.")  

def load_guests():                                   # Open the JSON file in read mode and return it as Python data
    with open(GUESTS_PATH, "r") as f:                
        return json.load(f)                          

def save_guests(data):                               # Open the JSON file in write mode and save the updated guest data
    with open(GUESTS_PATH, "w") as f:                
        json.dump(data, f, indent=2)                 

def show_green():                                    
    sense.clear(0, 255, 0)                           
    time.sleep(1)                                    
    sense.clear()                                    

def show_red():                                      
    sense.clear(255, 0, 0)                           
    time.sleep(1)                                    
    sense.clear()                                    

def capture_photo():                               
    print("Capturing image...")                      
    picam2.capture_file(IMAGE_PATH)                  
    print("Image saved to:", IMAGE_PATH)             

def read_qr():                                       # open the captured image file and try to detect and decode QR codes in the image
    img = Image.open(IMAGE_PATH)                     
    results = decode(img)                            

    if not results:                                  
        return None                                  

    return results[0].data.decode("utf-8")           # return the decoded QR text as a normal string

def check_guest(scanned_value):
    data = load_guests()                             
    guests = data.get("guests", [])                 

    for guest in guests:                             
        if guest.get("qr_value") == scanned_value:   # compare scanned QR to saved QR value
            if guest.get("checked_in") is True:      
                print("DUPLICATE ENTRY")             
                print(guest)                        
                show_red()                           
                return                               

            guest["checked_in"] = True               
            guest["checked_in_at"] = datetime.now().isoformat(timespec="seconds")  
            save_guests(data)                        

            print("VALID GUEST - CHECKED IN")       
            print(guest)                             
            show_green()                             
            return                                   

    print("INVALID GUEST")                           
    show_red()                                       

try:
    while True:                                     
        for event in sense.stick.get_events():       
            if event.action == "pressed" and event.direction == "middle":  
                print("Button pressed - starting QR scan")  
                capture_photo()                      

                scanned_value = read_qr()            # try to read a QR code from that photo

                if scanned_value is None:            # if no QR code was found
                    print("No QR code detected.")    
                    show_red()                       
                else:
                    print("Scanned QR:", scanned_value)  
                    check_guest(scanned_value)       # validate the scanned QR against JSON

        time.sleep(0.1)                              

except KeyboardInterrupt:                            
    print("Exiting...")                              

finally:                                             
    picam2.stop()                                    
    sense.clear()                                   
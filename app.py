from flask import Flask, render_template, request
import json
import os
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(BASE_DIR, "state", "guests.json")

def load_guests():
    try:
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"guests": []}

def save_guests(data):
    with open(STATE_PATH, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")

    data = load_guests()

    new_guest = {
        "name": name,
        "email": email,
        "registered_at": datetime.now().isoformat(timespec="seconds")
    }

    data["guests"].append(new_guest)
    save_guests(data)

    return f"Guest {name} registered successfully."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
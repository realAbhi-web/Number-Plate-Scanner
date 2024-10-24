from flask import Flask, render_template, request, url_for, redirect, session, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from api import rto_info, twilio_call, process_image
from priyanshu import convert_image_to_text
import http.client
import json
import os
import pytesseract
from PIL import Image
import base64
import io

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db' 
app.secret_key = 'your_secret_key_here'  # Set your secret key here
db=SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
car_dictionary={}



class Users(db.Model, UserMixin):
      id = db.Column(db.Integer, primary_key=True)
      name=db.Column(db.String(100), nullable=True)
      car_owner_name=db.Column(db.String(30))
      number_plate=db.Column(db.String,unique=True,nullable=False)
      phone_number=db.Column(db.String,unique=True,nullable=False)
      email=db.Column(db.String)
      car_model=db.Column(db.String)
      password=db.Column(db.String)
      fuel_type=db.Column(db.String(30))
      engine_number=db.Column(db.String(50))
      insurance_upto=db.Column(db.String(20))
      insurance_company=db.Column(db.String(30))
      vehicle_color=db.Column(db.String(10))
      seat_capacity=db.Column(db.String(10))
      manufacturing_time=db.Column(db.String(20))



# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route("/")
def home_page():
    return render_template('index.html')

def convert_base64_to_image(base64_string):
    # Decode the base64 image data
    image_data = base64.b64decode(base64_string.split(',')[1])
    
    # Convert the binary data to an image
    image = Image.open(io.BytesIO(image_data))
    
    return image


def convert_image_to_text(image):
    try:
        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return str(e)
    
@app.route("/photo")
def photo_page():
    return render_template("photo.html")

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        # Get the image data from the request
        data = request.get_json()
        image_data = data.get('image')

        if not image_data:
            return jsonify({"error": "No image data provided"}), 400

        # Convert the base64 image data to an actual image
        image = convert_base64_to_image(image_data)

        # Convert the image to text using pytesseract OCR
        text = convert_image_to_text(image)

        # Return the result
        return jsonify({'plate_text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# @app.route('/process_image', methods=['POST'])
# def handle_image():
#     if request.method == 'POST':
#         try:
#             # Retrieve the image from the JSON payload
#             data = request.json.get('image')  # Base64 encoded image

#             if not data:
#                 return jsonify({"error": "No image data provided"}), 400

#             # Process the image using the function from api.py
#             return process_image()

#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     return render_template("photo.html")

@app.route('/twilio_click', methods=["GET","POST"])
def call():
    car_dictionary = session.get('car_dictionary', {})
    
    # Check for the phone_number before trying to call
    phone_number = car_dictionary.get("phone_number")
    message=twilio_call(phone_number)

    return message

@app.route("/contact-us",methods=["GET","POST"])
def contact():
    return render_template("contact.html")


@app.route('/form', methods=["GET","POST"])
def form():
    if request.method=="POST":
        number_plate=request.form.get("form-page-number-plate")
        number_plate=number_plate.upper()
        print("number plate", number_plate)
        user = Users.query.filter_by(number_plate=number_plate).first()
        if user is not None:  # Check if a user was found
            session['car_dictionary'] = {
                "car_model": user.car_model,
                "owner_name": user.car_owner_name,
                "fuel_type": user.fuel_type,
                "number_plate": user.number_plate,
                "engine_number": user.engine_number,
                "insurance_upto": user.insurance_upto,
                "insurance_company": user.insurance_company,
                "vehicle_color": user.vehicle_color,
                "seat_capacity": user.seat_capacity,
                "manufacturing_time": user.manufacturing_time,
                "phone_number":user.phone_number
            }
            print("We are in database")
        else:
            session['car_dictionary']=rto_info(number_plate)
            print("we are in api")
        # print(number_plate)
        # print(car_dictionary['fuel_type'])
        # print(car_dictionary['car_model'])
        # print(car_dictionary['owner_name'])
        return render_template("search.html",car_dictionary=session.get('car_dictionary',{}))
        # print(number_plate)
        # print(type(number_plate))
    return render_template('form.html') 

@app.route("/log_in", methods=["GET","POST"])
def log_in():
    if request.method=="POST":
        user = Users.query.filter_by(email=request.form.get("email-log-in-form")).first()
        # Check if the password entered is the 
        # same as the user's password
        if user.password == request.form.get("password-log-in-form"):
            # Use the login_user method to log in the user
            login_user(user)
            flash('You have been logged in ,',user.name)
            # print(user)
            return redirect(url_for("home_page"))
        else:
            error="invalid email or password"
            return render_template("log_in.html",error=error)


    return render_template("log_in.html")

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        user = Users(
            name=request.form.get("name-form"),
            number_plate=request.form.get("number-plate-form").upper(),  # Convert to uppercase here
            phone_number=request.form.get("phone-number-form"),
            email=request.form.get("email-address-form"),
            car_model=request.form.get("car-form").upper(),  # Make sure car_model is also in uppercase
            password=request.form.get("password-form")  # Make sure to save the password
        )
        db.session.add(user)
        print("User added:")
        print("Number Plate:", user.number_plate)  # This should now be uppercase
        print("Phone Number:", user.phone_number)
        db.session.commit()
        return redirect("/")
    return render_template("Sign_up.html")

        # db.create_all() 
with app.app_context():
    try:
        db.create_all()
        print("Database created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == '__main__':
        app.run(debug=True)



        
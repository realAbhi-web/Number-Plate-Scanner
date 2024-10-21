from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user

import os
# from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
# login_manager = LoginManager()

# account_sid = "ACc7f300e177e5b63d1cb072ff94b8b139"
# auth_token = "386ff7cad41309df5b95350335a41024"
# client = Client(account_sid, auth_token)




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db' 
db=SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class Users(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      name=db.Column(db.String(100), nullable=True)
      number_plate=db.Column(db.Integer,unique=True,nullable=False)
      phone_number=db.Column(db.Integer,unique=True,nullable=False)
      email=db.Column(db.String)
      car=db.Column(db.String)
      password=db.Column(db.String)



# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route("/")
def home_page():
    return render_template('index.html')

@app.route("/log_in", methods=["GET","POST"])
def log_in():
    if request.method=="POST":
        user = Users.query.filter_by(email=request.form.get("email-log-in-form")).first()
        # Check if the password entered is the 
        # same as the user's password
        if user.email == request.form.get("password-log-in-form"):
            # Use the login_user method to log in the user
            login_user(user)
            print(user)
            return redirect(url_for("home_page"))


    return render_template("log_in.html")

@app.route("/sign_up", methods=["GET","POST"])
def sign_up():
    if request.method=="POST":
        user=Users(name=request.form.get("name-form"), number_plate=request.form.get("number-plate-form"), 
        phone_number=request.form.get("phone-number-form"), email=request.form.get("email-address-form"), car=request.form.get("car-form"), password=request.form.get("password-form"))
        db.session.add(user)
        db.session.commit()
        # print(user)
        return redirect("/")
    return render_template("Sign_up.html")

        # db.create_all() 
with app.app_context():
    db.create_all()

if __name__ == '__main__':
         
      #   call = client.calls.create(
      #       url="http://demo.twilio.com/docs/voice.xml",
      #       # twiml='<Response><Say>how can i help you BT </Say></Response',
      #       to="+919015426229",
      #       from_="+18583751040",
      #   )

      #   print(call.sid)
        app.run(debug=True)
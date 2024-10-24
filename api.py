# rto_info imports
import http.client
import json

# twillio imports
from twilio.rest import Client


def rto_info(number_plate):
    try:
        # Initialize connection
        conn = http.client.HTTPSConnection("rto-vehicle-information-india.p.rapidapi.com")

        # Correct the payload - no extra slash in the number_plate
        payload = f'{{"vehicle_no":"{number_plate}","consent":"Y","consent_text":"I hereby give my consent for Eccentric Labs API to fetch my information"}}'

        # Headers
        headers = {
            'x-rapidapi-key': "0b55234a7fmshe7ce95ba5e3dee3p1c6760jsne74bf1532498",  # Replace with your actual API key
            'x-rapidapi-host': "rto-vehicle-information-india.p.rapidapi.com",
            'Content-Type': "application/json"
        }

        # Make the request
        conn.request("POST", "/getVehicleInfo", payload, headers)
        
        # Get the response
        res = conn.getresponse()
        data = res.read()
        
        # Parse the response
        response = json.loads(data.decode("utf-8"))

        # Extract the 'data' key from the response safely
        answer = response.get('data', {})

        # Return relevant vehicle info
        return {
            "car_model": answer.get("maker_model", "Not Available"),
            "owner_name": answer.get("owner_name", "Not Available"),
            "registration_date": answer.get("registration_date", "Not Available"),
            "fuel_type": answer.get("fuel_type", "Not Available"),
            "engine_number": answer.get("engine_no", "Not Available"),
            "insurance_upto": answer.get("insurance_upto", "Not Available"),
            "insurance_company": answer.get("insurance_company", "Not Available"),
            "vehicle_color": answer.get("vehicle_color", "Not Available"),  # Corrected snake_case key
            "seat_capacity": answer.get("seat_capacity", "Not Available"),
            "manufacturing_time": answer.get("manufacture_month_year", "Not Available")
        }

    except Exception as e:
        print(f"Error fetching data: {e}")
        return {}


def twilio_call(number):
    account_sid = "ACc7f300e177e5b63d1cb072ff94b8b139"
    auth_token = "386ff7cad41309df5b95350335a41024"
    client = Client(account_sid, auth_token)
    
    try:
        call = client.calls.create(
            url="http://demo.twilio.com/docs/voice.xml",
            twiml='<Response><Say>how can i help you BT </Say></Response>',
            to=f"+91{number}",
            from_="+18583751040",
        )
        return "Your message has been successfully sent to"
    except Exception as e:
        return "Having Problems sending message to this number"


from flask import request, jsonify
import cv2
import numpy as np
import pytesseract
import base64

# from flask import request, jsonify
# import cv2
# import numpy as np
# import pytesseract
# import base64

def process_image():
    try:
        # Extract base64 image data from the request
        data = request.json['image']
        image_data = base64.b64decode(data.split(',')[1])  # Decode the base64 image

        # Convert the image data to a NumPy array and then to OpenCV format
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Convert to grayscale for plate detection
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        plate_cascade = cv2.CascadeClassifier('cascades/haarcascade_russian_plate_number.xml')

        plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

        plate_text = "No plate detected"
        for (x, y, w, h) in plates:
            img_roi = img[y:y + h, x:x + w]
            plate_text = pytesseract.image_to_string(img_roi, config='--psm 8')

        # Return the detected plate text
        return jsonify({'plate_text': plate_text})

    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'error': 'Failed to process image'}), 500







# def rto_info(number_plate):
#     try:
#         conn = http.client.HTTPSConnection("rto-vehicle-information-india.p.rapidapi.com")
#         payload = f'{{"vehicle_no":"{number_plate}/","consent":"Y","consent_text":"I hereby give my consent for Eccentric Labs API to fetch my information"}}'
#         headers = {
#             'x-rapidapi-key': "YOUR_API_KEY",
#             'x-rapidapi-host': "rto-vehicle-information-india.p.rapidapi.com",
#             'Content-Type': "application/json"
#         }

#         conn.request("POST", "/getVehicleInfo", payload, headers)
#         res = conn.getresponse()
#         data = res.read()
#         response = json.loads(data.decode("utf-8"))
#         answer = response.get('data', {})
        
#         # Extract information safely
#         return {
#             "car_model": answer.get("maker_model", "Not Available"),
#             "owner_name": answer.get("owner_name", "Not Available"),
#             "registration_date": answer.get("registration_date", "Not Available"),
#             "fuel_type": answer.get("fuel_type", "Not Available"),
#             "engine_number": answer.get("engine_no", "Not Available"),
#             "insurance_upto": answer.get("insurance_upto", "Not Available"),
#             "insurance_company": answer.get("insurance_company", "Not Available"),
#             "vehicle_color": answer.get("vehicle-color", "Not Available"),
#             "seat_capacity": answer.get("seat_capacity", "Not Available"),
#             "manufacturing_time": answer.get("manufacture_month_year", "Not Available")
#         }
#     except Exception as e:
#         print(f"Error fetching data: {e}")
#         return {}

m=rto_info("HP20C2190")
print(m)

import http.client
import json

def rto_info(number_plate):

    conn = http.client.HTTPSConnection("rto-vehicle-information-india.p.rapidapi.com")

    payload = f'{{"vehicle_no":"{number_plate}/","consent":"Y","consent_text":"I hereby give my consent for Eccentric Labs API to fetch my information"}}'

    headers = {
        'x-rapidapi-key': "1aa2717d94msh7dc3574e4cbd318p1eeeb7jsn84cd17dc5d5b",
        'x-rapidapi-host': "rto-vehicle-information-india.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    conn.request("POST", "/getVehicleInfo", payload, headers)

    res = conn.getresponse()
    data = res.read()
    response=json.loads(data.decode("utf-8"))
    answer=response.get('data',{})
    # print(answer)
    car_model=answer.get("maker_model")
    owner_name=answer.get("owner_name")
    registration_date=answer.get("registration_date")
    fuel_type=answer.get("fuel_type")
    engine_number=answer.get("engine_no")
    insurance_upto=answer.get("insurance_upto")
    insurance_company=answer.get("insurance_company")
    vehicle_color=answer.get("vehicle-color")
    seat_capacity=answer.get("seat_capacity")
    manufacturing_time=answer.get("manufacture_month_year")
    # print(car_model)
    # print(owner_name)/
       

    # print(data.decode("utf-8"))

# rto_info("HP20C2190")
import http.client

conn = http.client.HTTPSConnection("rto-vehicle-information-india.p.rapidapi.com")

payload = "{\"vehicle_no\":\"HP20E0002\",\"consent\":\"Y\",\"consent_text\":\"I hereby give my consent for Eccentric Labs API to fetch my information\"}"

headers = {
    'x-rapidapi-key': "b8059600d5mshe02ad4b22a4ebbep1d31aajsn15d92fe5ebbb",
    'x-rapidapi-host': "rto-vehicle-information-india.p.rapidapi.com",
    'Content-Type': "application/json"
}

conn.request("POST", "/getVehicleInfo", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
import requests
from datetime import datetime
import smtplib
import time
import os

MY_LAT = 30.748318 # Your latitude
MY_LONG = 76.747047 # Your longitude
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
    'tzid': 'Asia/kolkata'
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()

sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0]) #In 24-hour format,int will convert '01' to 1.

time_now = datetime.now()

def is_iss_overhead():
    # Your position is within +5 or -5 degrees of the ISS position,giving it a marginal error -->
    if (iss_latitude - 5 <= MY_LAT <= iss_longitude + 5) and (iss_longitude - 5 <= MY_LONG <= iss_longitude + 5):
        return True
    else:
        return False


#If night then we can see it clearly.
def is_night():
    if time_now.hour >= sunset_hour or time_now.hour <= sunrise_hour:
        return True
    else:
        return False
    #time_now.hour gives an integer between 0-23.

#Now send mail:
if is_iss_overhead() and is_night():
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(MY_EMAIL, MY_PASSWORD)
        smtp.sendmail(from_addr=MY_EMAIL,to_addrs=MY_EMAIL,msg = f'Subject:Look UP☝️!\nThe ISS is above you in the sky.')



#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.




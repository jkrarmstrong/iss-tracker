import requests
from datetime import datetime
import smtplib
import time


MY_EMAIL = "your_email@gmail.com"
MY_PASSWORD = "your_app_password"

MY_LONGITUDE = 00.0
MY_LATITUDE = 00.0


def is_iss_overhead():
    """Returns True if the ISS is currently overhead (+ or - 5 degrees)"""
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    # Get the current position of the ISS
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    # Check if the ISS is within 5 degrees of the user's location
    if MY_LONGITUDE-5 <= iss_longitude <= MY_LONGITUDE+5 and MY_LATITUDE-5 <= iss_latitude <= MY_LATITUDE+5:
        return True

def is_nightime():
    """Returns True if it's currently nighttime"""
    parameters = {
        "lat": MY_LATITUDE,
        "lng": MY_LONGITUDE,
        "formatted": 0,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    # Get the sunrise and sunset times in formatted time
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    current_time = datetime.now().hour

    # Check if it's currently nighttime (between sunrise and sunset)
    if current_time >= sunset or current_time <= sunrise:
        return True
    


def notify_user():
    """Send the user an email if the ISS is overhead and it's nighttime"""
    while True:
        time.sleep(60)
        if is_iss_overhead() and is_nightime():
            connection = smtplib.SMTP(MY_EMAIL, port=587)
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f"Subject: ISS Overhead\n\nThe ISS is currently overhead and!"
            )


# Run the main function to check for ISS overhead and send an email if necessary
notify_user()
import requests
import json
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

API_KEY = os.environ["TRACK_API_KEY"]
EMAIL_FROM = os.environ["EMAIL_USER"]
EMAIL_TO = os.environ["EMAIL_USER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASS"]

with open("trackings.json") as f:
    TRACKINGS = json.load(f)["trackings"]

def get_status(tracking):
    url = "https://api.17track.net/track/v2/GetTrackInfo"
    headers = {"17token": API_KEY}
    data = {"number": [tracking]}
    
    r = requests.post(url, json=data)
    res = r.json()

    try:
        events = res["data"][0]["track"][0]["z1"]
        last = events[0]
        return f"{last['a']} - {last['c']}"
    except:
        return "Sin información"

def build_report():
    lines = [f"Reporte - {datetime.now()}\n"]
    for t in TRACKINGS:
        status = get_status(t)
        lines.append(f"{t} → {status}")
    return "\n".join(lines)

def send_email(body):
    msg = MIMEText(body)
    msg["Subject"] = "Reporte de envíos"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)

if __name__ == "__main__":
    report = build_report()
    send_email(report)

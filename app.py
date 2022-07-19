from flask import Flask
import os
from twilio.rest import Client

app = Flask(__name__)

@app.route("/")
def index():
    # base page, gives user instruction
    return "<p>Welcome to the general page, direct to {env}/sendSMS to send a message</p>"


@app.route("/sendSMS")
def sendSMS():
    # account_sid = os.environ['AC9a514aeb37a22cc0629c8cfb4a47120f'] #def how it should be done
    # auth_token = os.environ['95f48287c0a7bdaeb9142958953aa05b'] #this is how it should be done
    account_sid = "AC9a514aeb37a22cc0629c8cfb4a47120f"
    # Your Auth Token from twilio.com/console
    auth_token = "95f48287c0a7bdaeb9142958953aa05b"
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="Join Earth's mightiest heroes. Like Kevin Bacon.",
        from_='+19854652607',
        to='+14255537653'
    )
    return "<p>sms sent<p>"

from flask import Flask
import os
from twilio.rest import Client

app = Flask(__name__)


@app.route("/")
def index():
    # base page, gives user instruction
    return "<p>Welcome to the general page, direct to {env}/sendSMS to send a message</p>"


def send_sms():
    # account_sid = os.environ['AC9a514aeb37a22cc0629c8cfb4a47120f'] #def how it should be done
    # auth_token = os.environ['bb3df30679555785dd9dad168f0e150d'] #this is how it should be done
    account_sid = "AC9a514aeb37a22cc0629c8cfb4a47120f"
    # Your Auth Token from twilio.com/console
    auth_token = "2eeecc861a097a92cb8a2cb228f4472e"
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="Go to https://auto-messaging-python.herokuapp.com/runLogic you fool, you'll get a message",
        from_='+19854652607',
        to='+12532234374'
    )
    # return "<p>sms sent<p>"


@app.route("/runLogic")
def run_logic():
    send_sms()
    return "<p>logic check<p>"

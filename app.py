from flask import Flask
import os
from twilio.rest import Client
from db import mysql

app = Flask(__name__)


@app.route("/")
def index():
    # base page, gives user instruction
    DB_host = os.getenv('CLEARDB_HOST')
    DB_user = os.getenv('CLEARDB_USER')
    DB_password = os.getenv('CLEARDB_PASSWORD')
    DB_database = os.getenv('CLEARDB_DATABASE')
    print(DB_host)
    print(DB_user)
    print(DB_password)
    print(DB_database)
    return "<p>Welcome to the general page, direct to {env}/sendSMS to send a message</p>"


def send_sms():
    # account_sid = os.environ['TWILIO_ACCOUNT_SID']
    # auth_token = os.environ['TWILIO_AUTH_TOKEN']
    sid_key = 'TWILIO_ACCOUNT_SID'
    auth_key = 'TWILIO_AUTH_TOKEN'

    account_sid = os.getenv(sid_key)
    auth_token = os.getenv(auth_key)

    print(account_sid, " this is sid")
    print(auth_token, " this is auth")

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="Go to https://auto-messaging-python.herokuapp.com/runLogic you fool, you'll get a message",
        from_='+19854652607',
        to='+14255537653'
    )
    # return "<p>sms sent<p>"
    # JOEY #: +12532234374
    # GRAHAM #: +14255537653

@app.route("/runLogic")
def run_logic():
    send_sms()
    return "<p>logic check<p>"

from flask import Flask
import os
from twilio.rest import Client
from db import mysql
from app import app
from routes import login

@app.route("/")
def health():
    return 'The Twilio Messaging Automation API is up and healthy!'

@app.route("/api/dbtest")
def test_DB():
    print("this shouldnlt run")
    try:
        with mysql:
            with mysql.cursor() as cursor:
                sql = "INSERT INTO `users` (`name`, `phone_number`, `password`) VALUES (%s, %s, %s)"
                cursor.execute(sql, ('test 2', '4255537655', 'testpass'))
                mysql.commit()

            with mysql.cursor() as cursor:
                sql = "SELECT `name` FROM `users` WHERE `phone_number`=%s"
                cursor.execute(sql, ('4255537655',))
                result = cursor.fetchone()
                print(result)
    finally:
        print("failed DB setup")

    return 'test db thing'



# def send_sms():
#     # account_sid = os.environ['TWILIO_ACCOUNT_SID']
#     # auth_token = os.environ['TWILIO_AUTH_TOKEN']
#     sid_key = 'TWILIO_ACCOUNT_SID'
#     auth_key = 'TWILIO_AUTH_TOKEN'
#
#     account_sid = os.getenv(sid_key)
#     auth_token = os.getenv(auth_key)
#
#     print(account_sid, " this is sid")
#     print(auth_token, " this is auth")
#
#     client = Client(account_sid, auth_token)
#
#     message = client.messages \
#         .create(
#         body="Go to https://auto-messaging-python.herokuapp.com/runLogic you fool, you'll get a message",
#         from_='+19854652607',
#         to='+14255537653'
#     )
#     # return "<p>sms sent<p>"
#     # JOEY #: +12532234374
#     # GRAHAM #: +14255537653

# @app.route("/runLogic")
# def run_logic():
#     send_sms()
#     return "<p>logic check<p>"


if __name__== "__main__":
    app.run()

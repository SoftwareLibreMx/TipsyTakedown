#!/bin/python

# Taken from: https://mailtrap.io/blog/flask-email-sending/

from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.sotolitolabs.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'changeme@sotolitolabs.com'
app.config['MAIL_PASSWORD'] = 'changeme'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)


@app.route("/")
def index():
    msg = Message(subject='Subject test', sender='changeme@sotolitolabs.com',
                  recipients=['changeme@sotolitolabs.com'])
    msg.body = "This is a test email"
    mail.send(msg)
    return "Message sent!"


if __name__ == '__main__':
    app.run(debug=True)

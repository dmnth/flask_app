#! /usr/bin/env python3

from flask import render_template
from flask_mail import Message
from app import mail
from app import app


def send_mail(subject, recipients, html_body):
    msg = Message(subject=subject, recipients=recipients)
    msg.html=html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_mail('[Not Done] Reset your password, bitch',
            recipients=[user.email],
#            text_body=render_template('email/reset_password.txt', user=user, token=token),
            html_body=render_template('email/reset_password.html', user=user, token=token))

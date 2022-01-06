#! /usr/bin/env python3

from flask_mail import Message
from app import mail

def send_mail(subject, recipients, html_body):
    msg = Message(subject=subject, recipients=recipients)
    msg.html=html_body
    mail.send(msg)

send_mail('testing', ['kborodin1@gmail.com', 'ingvrat@gmail.com'], '<h1> HeY TheRE wanna SEE nUdEs?') 

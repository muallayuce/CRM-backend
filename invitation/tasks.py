from django.core.mail import send_mail
from crm.celery import app

@app.task
def send_email_async(email, subject, body, from_email):
    send_mail(subject, body, from_email, [email], html_message=body, fail_silently=False)
    
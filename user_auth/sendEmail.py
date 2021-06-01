from django.conf import settings
import threading
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .utils import generate_token


# To speedup the sending email
class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


def sendEmail(request, newUser):
    current_site = get_current_site(request)
    email_subject = 'Activate your Account'
    message = render_to_string('auth/activate.html', {
        'user': newUser,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(newUser.pk)),
        'token': generate_token.make_token(newUser)
    })
    email_message = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [newUser.email]
    )

    EmailThread(email_message).start()

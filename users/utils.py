import random

from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from user_auth.sendEmail import EmailThread


def userFormValidate(email, f_name, l_name, user_type):
    response = {
        "error": False,
        "msg": ''
    }
    if (email is None or email == '') or (f_name is None or f_name == '') or (
            l_name is None or l_name == '') or (
                user_type is None or user_type == ''):
        response['error'] = True
        response['msg'] = "Please Fill all the fields"
        return response
    try:
        # print("Email: ", email)
        if User.objects.get(email=email):
            # print("User Exists")
            response['error'] = True
            response['msg'] = 'User already exists with this email'
            return response

    except User.DoesNotExist:
        # print("Unique User")
        pass

    return response


def sendEmailInvtn(request, newUser, password):
    current_site = get_current_site(request)
    email_subject = 'Invitation from ' + str(request.user)
    message = render_to_string('users/user_login_email.html', {
        'user': newUser,
        'domain': current_site.domain,
        'password': password,
    })
    email_message = EmailMessage(
        email_subject,
        message,
        settings.EMAIL_HOST_USER,
        [newUser.email]
    )

    EmailThread(email_message).start()


def generateRandomPass():
    characters = list('abcdefghijklmnopqrstuvwxyz')
    characters.extend('ABCDEFGHIJHIJKLMNOPQRSTUVWXYZ')
    characters.extend('0123456789')
    characters.extend('!@#$%^&*()-')

    thepassword = ''
    for i in range(10):
        thepassword += random.choice(characters)

    return thepassword

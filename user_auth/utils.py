from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_active))


generate_token = TokenGenerator()


def validateRegisterForm(data):
    response = {
        "msg": "",
        "error": False,
    }
    if (data['company_name'] is None or data['company_name'] == '') or (
        data['first_name'] is None or data['first_name'] == '') or (
            data['last_name'] is None or data['last_name'] == '') or (
                data['email'] is None or data['email'] == '') or (
                    data['password'] is None or data['password'] == ''):
        response['msg'] = "Please fill all the fields"
        response['error'] = True
        return response

    if len(data['password']) < 8:
        response['msg'] = "passwords should be atleast 6 characters long"
        response['error'] = True
        return response

    if data['password'] != data['password2']:
        response['msg'] = "Password do not matches"
        response['error'] = True
        return response

    try:
        user = User.objects.get(email=data['email'])
        if user and user.is_active is True:
            response['msg'] = "Email is taken"
            response['error'] = True
            return response

    except Exception as identifier:
        print("Exception: ", identifier)
        return response

    return response

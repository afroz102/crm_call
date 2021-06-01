from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile


class AddUserForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'last_name': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'email': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
        }


class AddUserForm2(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_type']

        widgets = {
            'user_type': forms.Select(attrs={
                'class': "form-control",
            }),
        }


class UpdateUserForm1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'last_name': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'email': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
        }

    # To disable the form fields in frontend(django won't look for it to update)
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm1, self).__init__(*args, **kwargs)
        self.fields['email'].disabled = True

# class UserEditForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password')

#     def __init__(self, *args, **kwargs):
#         super(UserEditForm, self).__init__(*args, **kwargs)
#         self.fields['username'].disabled = True
#         self.fields['email'].disabled = True


class UpdateUserForm2(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'profile_pic', 'user_type']
        widgets = {
            'phone': forms.TextInput(attrs={
                'type': 'text',
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
            'user_type': forms.Select(attrs={
                'class': "form-control",
                'autofocus': 'autofocus',
            }),
        }

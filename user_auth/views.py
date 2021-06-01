from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text


from .utils import validateRegisterForm, generate_token
from .sendEmail import sendEmail
from .decorators import unauthenticated_user
from users.models import Company, UserProfile


# Register View
@unauthenticated_user
def register_user(request):
    if request.method == 'POST':
        context = {'data': request.POST}

        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        validatePostForm = validateRegisterForm(request.POST)

        # print("validatePostForm: ", validatePostForm)

        if validatePostForm['error']:
            messages.add_message(
                request,
                messages.ERROR,
                validatePostForm['msg']
            )

            return render(request, 'auth/register.html', context, status=400)

        # Create a new User
        newUser, created = User.objects.get_or_create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        if created:
            newUser.set_password(password)
        newUser.is_active = False
        newUser.save()

        # Create a Company Object, user as  it's super admin
        companyObject = Company.objects.create(
            company_name=company_name,
            super_admin=newUser,
        )

        # Create a User Profile Object with user and agency
        UserProfile.objects.create(
            user=newUser,
            company=companyObject,
            user_type="0"
        )

        # Send registration email to user email
        sendEmail(request, newUser)

        # print("sendingEmail: ", sendingEmail)

        messages.add_message(
            request,
            messages.SUCCESS,
            'A link has been sent to your email.' +
            'click on the link to activate your account.'
        )

        return redirect('login')

    else:
        return render(request, 'auth/register.html')


def activate_account(request, uidb64, token):
    try:
        # checking if the uid is same as user.id sent from the host
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as identifier:
        print("Exception: ", identifier)
        user = None

    # if id matches set user as verified and save
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            'account activated successfully'
        )
        return redirect('login')

    # else return to activation failed page to show error message
    return render(request, 'auth/activate_failed.html', status=401)


@unauthenticated_user
def login_user(request):
    if request.method == "GET":
        return render(request, 'auth/login.html')

    if request.method == "POST":
        context = {
            'data': request.POST,
        }

        # username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == '' or password == '':
            messages.add_message(
                request,
                messages.ERROR,
                'Please fill all the fields'
            )
            return render(request, 'auth/login.html', context, status=401)

        user = authenticate(request, username=email, password=password)
        # print("user: ", user)

        if not user:
            messages.add_message(
                request,
                messages.ERROR,
                'Email or Password is Wrong'
            )
            return render(request, 'auth/login.html', context, status=401)

        login(request, user)

        return redirect('home')


def logoutUser(request):
    logout(request)
    return redirect('login')

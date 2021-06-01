from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import render, redirect

from .models import UserProfile
from . import forms

from .utils import userFormValidate, generateRandomPass, sendEmailInvtn


@login_required(login_url='login')
def getAllUser(request):
    user = request.user
    loggedInUser = UserProfile.objects.get(user=user)
    users = UserProfile.objects.filter(
        company=loggedInUser.company.id, is_deleted=False)

#     from django.core import serializers
#
#     # assuming obj is a model instance
#     serialized_obj = serializers.serialize('json', [user])
#     print(serialized_obj)

    context = {
        "loggedInUser": loggedInUser,
        "users": users,
    }
    return render(request, 'users/all_users.html', context)


@login_required(login_url='login')
def addUser(request):
    user = request.user
    loggedInUser = UserProfile.objects.get(user=user)
    company = loggedInUser.company

    form1 = forms.AddUserForm1()
    form2 = forms.AddUserForm2()
    context = {
        "loggedInUser": loggedInUser,
        "form1": form1,
        "form2": form2
    }

    if request.method == 'POST':
        context = {
            "loggedInUser": loggedInUser,
            "form1": form1,
            "form2": form2,
            'data': request.POST
        }
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_type = request.POST.get('user_type')
        password = generateRandomPass()

        validateForm = userFormValidate(
            email, first_name, last_name, user_type)

        if validateForm['error']:
            messages.add_message(request, messages.ERROR, validateForm['msg'])
            return render(request, 'users/add_user.html',
                          context, status=400)

        user = User.objects.create_user(username=email, email=email)
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Create a userprofile with user and agency
        UserProfile.objects.create(
            user=user, company=company, user_type=user_type)

        # print("neUserProfile: ", neUserProfile)

        # Send invitation mail to user email
        sendEmailInvtn(request, user, password)

        messages.add_message(
            request,
            messages.SUCCESS,
            'The Invitaion link has been sent to user.'
        )
        return render(request, 'users/add_user.html',
                      context, status=200)

    return render(request, 'users/add_user.html', context)


@login_required(login_url='login')
def userProfile(request, user_pk):
    user = request.user
    loggedInUser = UserProfile.objects.get(user=user)

    userProfile = UserProfile.objects.get(id=user_pk)
    if loggedInUser.company != userProfile.company:
        return JsonResponse({
            "status": "Error",
            "msg": "You are not authorized"
        })

    form1 = forms.UpdateUserForm1(instance=userProfile.user)  # user
    form2 = forms.UpdateUserForm2(instance=userProfile)  # UserProfile
    # Userprofile Agency Mapping
    # form3 = forms.AddUserForm2()

    context = {
        'form1': form1,
        'form2': form2,
        # "form3": form3,
        "userProfile": userProfile,
        "loggedInUser": loggedInUser,
    }
    if request.method == 'POST':
        # userStatus = request.POST['active_status']
        form1Data = forms.UpdateUserForm1(
            request.POST, instance=userProfile.user)
        form2Data = forms.UpdateUserForm2(
            request.POST, request.FILES, instance=userProfile)
        # form3Data = forms.AddInUserForm2(request.POST)

        print("form1 Data: ", form1Data)

        if form1Data.is_valid() and form2Data.is_valid():
            print("form is valid")
            form1Data.save()
            form2Data.save()
            # if userStatus == 'inactive':
            #     form1Data.is_active = False
            # form1Data.save()
            return redirect('user_profile', user_pk=user_pk)

    return render(request, 'users/user_profile.html', context)


@login_required(login_url='login')
def deleteUser(request, user_pk):
    userProfile = UserProfile.objects.get(id=user_pk)

    if request.method == 'POST':
        userProfile.is_deleted = True
        userProfile.save()
        # Set active status to false
        userProfile.user.is_active = False
        userProfile.user.save()
        return redirect('get_all_user')


# @login_required(login_url='login')
# def updateUser(request, user_pk):
#     loggedInUser = UserProfile.objects.get(user=request.user)
#     userProfile = UserProfile.objects.get(id=user_pk)
#     form1 = forms.UpdateUserForm1(instance=userProfile.user)
#     form2 = forms.UpdateUserForm2(instance=userProfile)
#     context = {
#         "loggedInUser": loggedInUser,
#         'form1': form1,
#         'form2': form2,
#         'userProfile': userProfile,
#     }
#
#     if request.method == 'POST':
#         form1 = forms.UpdateInUserForm1(
#             request.POST, instance=userProfile.user)
#         form2 = forms.UpdateInUserForm2(
#             request.POST, request.FILES, instance=userProfile)
#
#         print("form2 Data: ", form2)
#         if form1.is_valid() and form2.is_valid():
#             print("form is valid")
#             form1.save()
#             form2.save()
#             return redirect('/')
#     return render(request, 'users/update_user_details.html', context)


@login_required(login_url='login')
def updateUserPassword(request, user_pk):
    return JsonResponse({"msg": "hello"})

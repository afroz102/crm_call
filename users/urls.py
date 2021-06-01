from django.urls import path
# from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('users/', views.getAllUser, name="get_all_user"),
    path('user/add/', views.addUser, name="add_user"),


    # path('user/<int:user_pk>/update/', views.updateUser, name="update_user"),
    path('user/<int:user_pk>/delete/', views.deleteUser, name="delete_user"),

    path('user/<int:user_pk>/password/update/',
         views.updateUserPassword, name="update_password"),

    path('user/<int:user_pk>/', views.userProfile, name="user_profile"),

]

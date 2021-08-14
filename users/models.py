import uuid
from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    super_admin = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True)

    company_name = models.CharField(max_length=200)
    api_key = models.CharField(max_length=50, unique=True, default=uuid.uuid4())
    phone = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=50, blank=True)
    logo = models.ImageField(
        upload_to='company_logo/', default="default/dummy-logo.jpeg",)

    # to store logic for rendering the stage
    stage_reorder_logic = models.TextField(blank=True)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name


class UserProfile(models.Model):
    USERTYPE = (
        ('0', 'Super Admin'),
        ('1', 'Manager'),
        ('2', 'Normal User'),
        ('3', 'type-3'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pic/', default="default/profile-dum.jpg")

    user_type = models.CharField(max_length=50, choices=USERTYPE, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user.first_name:
            return self.user.first_name + ' ' + self.user.last_name
        return str(self.id)

    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

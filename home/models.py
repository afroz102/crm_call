from django.db import models
from django.contrib.auth.models import User
from users.models import Company


class LeadStage(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    stage_label = models.CharField(max_length=50)

    # to store logic, for rendering the leads in the stage
    leads_reorder_logic = models.TextField(blank=True)

    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stage_label


class CustomField(models.Model):
    FIELD_TYPE = (
        ('text', 'Text'),
        ('number', 'Number'),
        ('email', 'Email'),
        ('drop_down', 'Drop Down'),
        ('radio', 'Radio'),
        ('date', 'Date'),
        ('time', 'Time'),
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    field_title = models.CharField(max_length=50)
    field_type = models.CharField(
        max_length=50, choices=FIELD_TYPE, default="Text")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.field_title


class CustomFieldChoise(models.Model):
    custom_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    choise_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.choise_name


# For storing gmail credential
class GmailCredential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=200, null=True)
    refresh_token = models.CharField(max_length=200, null=True)
    token_uri = models.CharField(max_length=200, null=True)
    client_id = models.CharField(max_length=200, null=True)
    client_secret = models.CharField(max_length=200, null=True)
    id_token = models.CharField(max_length=200, null=True)
    scopes = models.CharField(max_length=1000, null=True)
    expiry = models.DateTimeField(blank=True, null=True)
    valid = models.BooleanField(default=True)

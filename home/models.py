from django.db import models
from users.models import Company
from django.contrib.auth.models import User


class LeadStage(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    stage_label = models.CharField(max_length=50)

    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.stage_label


class StageIndexOrder(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    reorder_string = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company.company_name + '-stage order'


class StageElementIndexLogic(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    stage = models.OneToOneField(LeadStage, on_delete=models.CASCADE)
    element_index_logic = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stage.stage_label


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


class CustomFieldAnswer(models.Model):
    custum_field = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    title_answer = models.CharField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.custum_field.field_title}-answer'

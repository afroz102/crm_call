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


class StageElementIndexLogic(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    stage = models.OneToOneField(LeadStage, on_delete=models.CASCADE)
    element_index_logic = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

from django.contrib.auth.models import User
from django.db import models
from home.models import LeadStage
from users.models import Company


class Lead(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    stage = models.ForeignKey(LeadStage, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=50)
    email = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    designation = models.CharField(max_length=50, blank=True)
    source = models.CharField(max_length=50, blank=True)

    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LeadContact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=50)
    email = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    designation = models.CharField(max_length=50, blank=True)

    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.contact_person


class LeadNote(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    note = models.TextField()

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LeadTask(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    task = models.TextField()

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LeadProfileLog(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    log = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lead.title + '-Log-' + str(self.id)

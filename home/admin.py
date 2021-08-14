from django.contrib import admin

from . import models

admin.site.register(models.LeadStage)
admin.site.register(models.CustomField)
admin.site.register(models.CustomFieldChoise)
admin.site.register(models.GmailCredential)

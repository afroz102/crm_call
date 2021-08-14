from django.contrib import admin

from . import models


admin.site.register(models.Lead)
admin.site.register(models.LeadNote)
admin.site.register(models.LeadTask)
admin.site.register(models.LeadProfileLog)
admin.site.register(models.LeadContact)
admin.site.register(models.CustomFieldAnswer)

from django.contrib import admin

from . import models

admin.site.register(models.LeadStage)
admin.site.register(models.StageIndexOrder)
admin.site.register(models.StageElementIndexLogic)
admin.site.register(models.CustomField)
admin.site.register(models.CustomFieldChoise)
admin.site.register(models.CustomFieldAnswer)

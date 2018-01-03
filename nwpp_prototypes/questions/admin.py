from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Profile)
admin.site.register(models.Badge)
admin.site.register(models.Notification)
admin.site.register(models.Vote)
admin.site.register(models.Comment)
admin.site.register(models.Flag)

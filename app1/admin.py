from django.contrib import admin

from app1 import models

# Register your models here.
admin.site.register(models.Login)
admin.site.register(models.Services)
admin.site.register(models.Worker)
admin.site.register(models.Customer)
admin.site.register(models.Appointment)
admin.site.register(models.Complaint)
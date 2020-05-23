from django.contrib import admin
from orders import models

# Register your models here.
admin.site.register(models.Table)
admin.site.register(models.Check)
admin.site.register(models.Order)
admin.site.register(models.Status)

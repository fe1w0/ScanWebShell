from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.ModelWithFileField)
admin.site.register(models.ScanTaskField)
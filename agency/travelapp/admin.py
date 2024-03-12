from xml.parsers.expat import model
from django.contrib import admin
from .models import PackageDetails

# Register your models here.
class PackageDetailsAdmin(admin.ModelAdmin):
    list_display=('packagename','amount')
admin.site.register(PackageDetails,PackageDetailsAdmin)


from django.contrib import admin
from .models import Profile, Category

# Register your models here.

admin.site.site_header = Profile.objects.get(id=1).name
admin.site.site_title = Profile.objects.get(id=1).name + "Yönetim portalı"
admin.site.register(Profile)
admin.site.register(Category)
from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Profile(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(default='rest_def.jpg', upload_to='profile_pics/')
    cover = models.ImageField(default='cover_def.jpg', upload_to='cover_pics/')
    openTime = models.CharField(max_length=10)
    closeTime = models.CharField(max_length=10)
    tiktok = models.URLField(max_length=200, null=True, blank=True)
    whatsapp = models.URLField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    googleMaps = models.URLField(max_length=200, null=True, blank=True)
    currency = models.CharField(max_length=10, default='TL')


    class Meta:
        verbose_name = "Profile"

class Category(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

from django.db import models
from django.utils import timezone
from pages.models import Category



class Product(models.Model):

    title = models.CharField(max_length=100, default='عنوان الوجبة')
    image = models.ImageField(default='meal_def.jpg', upload_to='product_pics/')
    description = models.TextField(default='وصف الوجبة')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    buyingMassage = models.TextField(default='رسالة الشراء')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sender_id = models.IntegerField(default=1)

    def __str__(self):
        return self.title
    
class Hotdeals(models.Model):

    
    title = models.CharField(max_length=100)
    image = models.ImageField(default='hotDeal_def.jpg', upload_to='hotdeal_pics/')
    description = models.TextField()
    oldPrice = models.DecimalField(max_digits=6, decimal_places=2)
    newPrice = models.DecimalField(max_digits=6, decimal_places=2)
    buyingMassage = models.TextField(default='رسالة الشراء')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sender_id = models.IntegerField()
    end_time = models.DateTimeField()
    

    def __str__(self):
        return self.title
    
    def check_and_delete_expired_deal(self):
        """
        Check if the deal has expired based on the `end_time`.
        If it has expired, delete the instance.
        """
        now = timezone.now()
        if self.end_time <= now:
            self.delete()
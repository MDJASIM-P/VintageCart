from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ClothModel(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    details = models.CharField(max_length=500)
    sizes = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL')
    )
    size = models.CharField(max_length=100, choices=sizes)
    image = models.ImageField(upload_to='cloths')
    likes = models.ManyToManyField(User, related_name="pro_likes")
    def total_likes(self):
        return self.likes.count()
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    product = models.ForeignKey(ClothModel, on_delete=models.CASCADE) 
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=100, default="Cart")

    def __str__(self):
        return self.product

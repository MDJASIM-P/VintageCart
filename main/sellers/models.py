from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from product.models import ClothModel
# Create your models here.

 
class MessageModel(models.Model):
    email = models.EmailField()
    message = models.TextField(max_length=500)
    datetime = models.DateTimeField(default=timezone.now())

class FeedbackModel(models.Model):
    pro = models.ForeignKey(ClothModel, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='')
    feedback = models.TextField(max_length=500)
    likes = models.ManyToManyField(User, related_name="feed_likes", blank=True,null=True)
    datetime = models.DateTimeField(default=datetime.now().strftime("%Y%m%d %H:%M:%S"))

class Report(models.Model):
    feedback = models.ForeignKey(FeedbackModel, on_delete=models.CASCADE)
    user = models.IntegerField()
    report  = models.CharField(max_length=100)
    datetime = models.DateTimeField(default=datetime.now())
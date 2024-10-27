from datetime import datetime
import json
from django.db import models
from userprofile.models import UserProfile
from django.contrib.auth.models import User



# Create your models here.


class Offer(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    image = models.FileField(upload_to='', blank=True, null=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)
    min_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    min_delivery_time = models.IntegerField(blank=True, null=True)

    # def __str__(self):
    #     return f"({self.id}) {self.title}"

class Feature(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    

    def __str__(self):
        return f"{self.title}"
    
class Detail(models.Model):
    title = models.CharField(max_length=30)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_type = models.CharField(max_length=10)
    features = models.ManyToManyField(Feature, related_name='features_set')


class OfferDetail(Detail):
    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
  
    
    def __str__(self):
        return f"({self.id}) {self.title}"
    


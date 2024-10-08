from django.db import models
from userprofile.models import UserProfile
from django.contrib.auth.models import User


# Create your models here.


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    image = models.FileField(upload_to='', blank=True, null=True)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    min_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    min_delivery_time = models.IntegerField(blank=True, null=True)

    # def __str__(self):
    #     return f"({self.id}) {self.title}"

class Detail(models.Model):
    offer = models.ForeignKey(Offer, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_type = models.CharField(max_length=10)
    features = models.TextField(max_length=200, blank=True, null=True)
  

    def __str__(self):
        return f"({self.id}) {self.title}"
    
# class Feature(models.Model):
#     details = models.ForeignKey(Detail, related_name='features', null=True, on_delete=models.CASCADE)
#     title = models.CharField(max_length=30, null=True, blank=True)

#     def __str__(self):
#          return self.title
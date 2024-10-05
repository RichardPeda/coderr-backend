from django.db import models
from userprofile.models import UserProfile


# Create your models here.
class Offer(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    image = models.FileField(upload_to='')
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    min_price = models.DecimalField(max_digits=4, decimal_places=2)
    min_delivery_time = models.DecimalField(max_digits=2, decimal_places=0)

    def __str__(self):
        return f"({self.id}) {self.title}"

class Features(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
         return f"({self.id}) {self.title}"

class OfferDetails(models.Model):
    title = models.CharField(max_length=30)
    revisions = models.DecimalField(max_digits=2, decimal_places=0)
    delivery_time_in_days = models.DecimalField(max_digits=2, decimal_places=0)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    offer_type = models.CharField(max_length=10)
    features = models.ManyToManyField(Features)

    def __str__(self):
        return f"({self.id}) {self.title}"
from django.db import models
from django.contrib.auth.models import User

from offer.models import Feature, OfferDetail, Detail
from userprofile.models import UserProfile




class Order(models.Model):
    PROGRESS = "in_progress"
    COMPLETE = "completed"
   
    STATUS_COICES = {
        PROGRESS: "in_progress",
        COMPLETE: "completed",
      
    }   
    offer_detail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name='order_offer_detail')
    customer_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_customer_user')
    business_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_business_user')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_COICES, default=PROGRESS)







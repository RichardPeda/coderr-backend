from django.db import models
from django.contrib.auth.models import User

from offer.models import Feature, OfferDetail, Detail
from userprofile.models import UserProfile




class Order(Detail):
    customer_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_customer_user')
    business_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_business_user')
    # title = models.CharField(max_length=100)
    # revisions = models.DecimalField()
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now_add=True)
    # min_price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    # min_delivery_time = models.IntegerField(blank=True, null=True)
    # features = models.ManyToManyField(Feature, related_name='features_set')



#      "id": 2,
#   "customer_user": 1,
#   "business_user": 3,
#   "title": "Website Development",
#   "revisions": 5,
#   "delivery_time_in_days": 10,
#   "price": 500.00,
#   "features": ["Homepage", "Responsive Design"],
#   "offer_type": "premium",
#   "status": "in_progress",
#   "created_at": "2024-09-30T12:30:00Z",
#   "updated_at": "2024-09-30T12:30:00Z"






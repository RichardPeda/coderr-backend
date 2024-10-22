from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    BUSINESS = "business"
    CUSTOMER = "customer"
   
    TYPE_CHOICES = {
        BUSINESS: "business",
        CUSTOMER: "customer",
      
    }
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile_user')
    file = models.FileField(upload_to='uploads/userprofile/', null=True, blank=True)
    location = models.CharField(max_length=20)
    tel = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    working_hours = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=CUSTOMER)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"({self.id}) {self.user}"
    

class Review(models.Model):
    business_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='review_business_user')
    reviewer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='review_reviewer')
    rating = models.IntegerField()
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


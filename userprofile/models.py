from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    BUSINESS = "bu"
    CUSTOMER = "cu"
   
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
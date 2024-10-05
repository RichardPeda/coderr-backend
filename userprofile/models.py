from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/userprofile/')
    location = models.CharField(max_length=20)
    tel = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    working_hours = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
from rest_framework import serializers

from userprofile.models import UserProfile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']
        # fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)


    class Meta:
        model = UserProfile
        fields = '__all__'
        
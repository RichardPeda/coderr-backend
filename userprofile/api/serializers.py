from rest_framework import serializers

from userprofile.models import Review, UserProfile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','first_name', 'last_name', 'username']




class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data is not None:
            serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if serializer.is_valid():
                serializer.save()           
        return instance

class ReviewSerializer(serializers.ModelSerializer):
      class Meta:
        model = Review
        fields = '__all__'



{
    "user": {
        "first_name": "Richie"
     
    }
}
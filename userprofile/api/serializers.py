import json
from rest_framework import serializers

from userprofile.models import Review, UserProfile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','first_name', 'last_name', 'username']

class UserFlattenSerializer(serializers.ModelSerializer):
    
    user = serializers.SerializerMethodField('get_alternate_name')
    class Meta:
        model = User
        fields = ['user','first_name', 'last_name', 'username', 'email']
        
        
    def get_alternate_name(self, obj):
        return obj.pk
    
    
        
class UserGetProfileSerializer(serializers.ModelSerializer):
    user = UserFlattenSerializer()
    class Meta:
        model = UserProfile
        exclude = ['id']
    
    def to_representation(self, obj):
        """Move fields from profile to user representation."""
        representation = super().to_representation(obj)
        profile_representation = representation.pop('user')
        for key in profile_representation:
            representation[key] = profile_representation[key]
        return representation
    
    def validate_user(self, value):
        return value
    
    def update(self, instance, validated_data):
        instance.user.first_name = self.context['request'].POST.get('first_name', instance.user.first_name)
        instance.user.last_name = self.context['request'].POST.get('last_name', instance.user.last_name)
        instance.user.email = self.context['request'].POST.get('email', instance.user.email)
        instance.user.save()
                
        instance.location = validated_data.get('location', instance.location)
        instance.tel = validated_data.get('tel', instance.tel)
        instance.description = validated_data.get('description', instance.description)
        instance.working_hours = validated_data.get('working_hours', instance.working_hours)
        instance.save()
        return instance

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
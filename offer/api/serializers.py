from rest_framework import serializers

from offer.models import Feature, Offer, Detail
from userprofile.api.serializers import UserProfileSerializer, UserSerializer
from userprofile.models import UserProfile
from django.contrib.auth.models import User
from rest_framework.fields import ListField
from drf_writable_nested.serializers import WritableNestedModelSerializer



class FeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feature
        fields = '__all__'

class OfferDetailUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Detail
        fields = ['id', 'url']
class DetailSerializer(serializers.ModelSerializer):
    features = serializers.StringRelatedField(many=True)
    class Meta:
        model = Detail
        fields = ['id', 'title','revisions','delivery_time_in_days','price','offer_type','features' ]
        depth = 1

class OfferGetSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    details = OfferDetailUrlSerializer(many=True)
    class Meta:
        model = Offer
        fields = ['id', 'user','title', 'image', 'description', 'created_at', 'updated_at',  'details', 'min_price', 'min_delivery_time', 'user_details']


class FeatureSetSerializer(serializers.ListField):
    title = serializers.CharField()
    def to_representation(self, data):
        return [
            self.child.to_representation(item.title) for item in data.all()
        ]

class DetailCreateSerializer(serializers.ModelSerializer):
    # features =   FeatureSerializer(many=True)
    features =   FeatureSetSerializer()
    # features =   serializers.ListField(child=serializers.CharField(), write_only=True)
   
    class Meta:
        model = Detail
        fields = ['id', 'title','revisions','delivery_time_in_days','price','offer_type', 'features',  ]
        # fields = '__all__'

    def validate_features(self, value):
        feature_id, created = Feature.objects.get_or_create(title=value)
        feature = Feature.objects.filter(title=value).only('id').first()

        print(f"feature{feature}")
        return feature
    

class OfferCreateSerializer(serializers.ModelSerializer):
    details = DetailCreateSerializer(many=True)
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ["user"]
  
   
    def create(self, validated_data):
       
        val_details = validated_data.pop('details')
        
        offer = Offer.objects.create(**validated_data)

        for val_detail in val_details:
            val_features = val_detail.pop('features')
            print(f"val_features{val_features}")
            detail = Detail.objects.create(offer=offer, **val_detail)
            detail.features.add(val_features)
            
            # detail.features.set(feature)
        
      
        return offer

    
    



class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

 


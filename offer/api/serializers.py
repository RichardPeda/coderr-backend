from rest_framework import serializers

from offer.models import Offer, Detail
from userprofile.api.serializers import UserProfileSerializer, UserSerializer
from userprofile.models import UserProfile
from django.contrib.auth.models import User
from rest_framework.fields import ListField

class OfferDetailUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Detail
        fields = ['id', 'url']

# class FeatureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Feature
#         fields = ['title']

class DetailSerializer(serializers.ModelSerializer):
    features = serializers.StringRelatedField(many=True)
    class Meta:
        model = Detail
        # fields = '__all__'
        fields = ['id', 'title','revisions','delivery_time_in_days','price','features','offer_type']

class OfferGetSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    # details = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='offer_detail_view')
    details = OfferDetailUrlSerializer(many=True)
    # details = DetailSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user','title', 'image', 'description', 'created_at', 'updated_at',  'details', 'min_price', 'min_delivery_time', 'user_details']







"""
*For creating a Offer detail with features
"""
class OfferDetailCreateSerializer(serializers.ModelSerializer):
    features = serializers.ListField(child=serializers.CharField(), write_only=True)
    class Meta:
        model = Detail
        # fields = '__all__'
        fields = ['id','title','revisions','delivery_time_in_days','price','features','offer_type']

    # def validate_features(self, value):
    #     for i in value:
    #         # features, created = Feature.objects.get_or_create(title=i)
    #         print(f"features {features}")
    #     return features
    
    def create(self, validated_data):
        feature_ids = validated_data.pop('features')
        offerdetails = Detail.objects.create(**validated_data)
        # features = Feature.objects.filter(title=feature_ids)
        # offerdetails.features.set(features)
        print(offerdetails)
        return offerdetails


# class FeatureSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Feature
#         fields = '__all__'

class StringArrayField(ListField):
    """
    String representation of an array field.
    """
    def to_representation(self, obj):
        obj = super().to_representation(self, obj)
        # convert list to string
        return ",".join([str(element) for element in obj])

    def to_internal_value(self, data):
        data = str(data).split(",")  # convert string to list
        return super().to_internal_value(data)

class DetailCreateSerializer(serializers.ModelSerializer):
    features = StringArrayField()
    # features = serializers.ListField(child=serializers.CharField(style={'base_template': 'textarea.html'}), write_only=True)
    # features = serializers.JSONField(binary=True) 
    class Meta:
        model = Detail
        # fields = '__all__'
        # fields = ['id', 'title','revisions','delivery_time_in_days','price','features','offer_type']
        fields = ['id', 'title','revisions','delivery_time_in_days','price','offer_type', 'features']

    # def validate_features(self, values):
    #     list_of_shortened_str = [value for value in values]
    #     print(f"features {list_of_shortened_str}")
    #     return list_of_shortened_str
    

    # def validate(self, attrs):
    #     return super().validate(attrs)

    # def create(self, validated_data):
    #     # details_id = validated_data.pop('details')
    #     feature_id = validated_data.pop('features')
    #     details = Detail.objects.create(**validated_data)
    #     # feature = Detail.objects.filter(id=details_id)
    #     feature = Feature.objects.filter(id=feature_id)
    #     details.feature.set(feature)
    #     # offer.details.feature.set(feature)
    #     # print(offerdetails)

    #     print(f"details {details.id}")


        # return details

class OfferCreateSerializer(serializers.ModelSerializer):
    # details = serializers.ListField(child=DetailCreateSerializer(), write_only=True)
    details = DetailCreateSerializer(many=True, write_only=True)
    # features = serializers.ListField(child=serializers.CharField(), write_only=True)
    # features = FeatureSerializer(many=True, write_only=True)
   
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ["user"]
  
    # def validate_features(self, values):
    #     # for i in values:
    #     #     features, created = Feature.objects.get_or_create(title=i)
    #     print(f"features {values}")
    #     return values

    def create(self, validated_data):
        print(f'data 1{validated_data}')
        # details_id = validated_data.pop('features')
        details_id = validated_data.pop('details')
       
        
        print(f'data 2{validated_data}')
        # print(f'data 3{details_id}')
       
        offer = Offer.objects.create(**validated_data)
        # features_id = details_id.pop('features')
        for ids in details_id:
            Detail.objects.create(offer=offer, **ids)
      
      
        return offer

    
    






 



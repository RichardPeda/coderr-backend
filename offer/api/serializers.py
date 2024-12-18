from rest_framework import serializers
from offer.models import Feature, Offer, OfferDetail
from userprofile.api.serializers import GetUserOffersSerializer, UserFlattenSerializer
from django.utils import timezone

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'

class OfferDetailUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
class DetailSerializer(serializers.ModelSerializer):
    features = serializers.StringRelatedField(many=True)
    class Meta:
        model = OfferDetail
        fields = ['id', 'title','revisions','delivery_time_in_days','price','offer_type','features' ]
        depth = 1

class OfferGetSerializer(serializers.ModelSerializer):
    user_details = GetUserOffersSerializer(source='user', read_only=True)
    details = OfferDetailUrlSerializer(many=True)
    class Meta:
        model = Offer
        fields = ['id', 'user','title', 'image', 'description', 'created_at', 'updated_at',  'details', 'min_price', 'min_delivery_time', 'user_details']

class FeatureCreateSerializer(serializers.ListField):
    title = serializers.CharField()

    def to_representation(self, data):
        """
        Change the representation of the features, that only the titles will be returned.
        """
        return [
            self.child.to_representation(item.title) for item in data.all()
        ]
        
class DetailCreateSerializer(serializers.ModelSerializer):
    features =   FeatureCreateSerializer()  
    class Meta:
        model = OfferDetail
        fields = ['id', 'title','revisions','delivery_time_in_days','price','features','offer_type', ]

    def validate_features(self, value):
        """
        Validation of the features. It is not allowed to post empty features.
        """
        if len(value) == 0:
            raise serializers.ValidationError("feature cannot be empty")
        new_val = []
        for val in value:
            feature_id, created = Feature.objects.get_or_create(title=val)
            new_val.append(feature_id)
        return new_val
    
    def validate_delivery_time_in_days(self,value):  
        """
        Validate the delivery_time, that there are no negative values given.
        """      
        if value <= 0:
            raise serializers.ValidationError("delivery time can only be positive integers")
        return value

class OfferCreateSerializer(serializers.ModelSerializer):
    details = DetailCreateSerializer(many=True)
    class Meta:
        model = Offer
        fields = ['id', 'title', 'image','description','details',]
        read_only_fields = ["user"]
      
    def validate_details(self, value):
        """
        Validating the details. Exactly three details must be given to the serializer.
        """
        if len(value) != 3:
            raise serializers.ValidationError('When creating an offer, exactly three details must be provided')
        matches = ['basic', 'standard','premium']
        for val in value:
            if matches.count(val['offer_type']) == 1:
                matches.remove(val['offer_type'])
            else:
                raise serializers.ValidationError("offer_type must be used once each \"basic\", \"standard\" and \"premium\"")
        return value
   
    def create(self, validated_data):
        """
        Creates an offer with the nested child objects.
        The features are allready created in the validator of the DetailCreateSerializer
        First create an offer and get the min price and the min delivery time of the details and save them to the offer.
        After that, the details will be created and the relations will be set.
        Feature related to Detail. Detail related to Offer.
        """
        try:
            
            val_details = validated_data.pop('details')
            offer = Offer(**validated_data)
            prices=[]
            delivery_time=[]
            for val_detail in val_details:
                prices.append(val_detail['price'])
                delivery_time.append(val_detail['delivery_time_in_days'])
            offer.min_price = min(prices)
            offer.min_delivery_time = min(delivery_time)
            offer.save()
            for val_detail in val_details:
                val_features = val_detail.pop('features')
                detail = OfferDetail.objects.create(offer=offer, **val_detail)
                for val in val_features:
                    detail.features.add(val) 
            return offer
        except:
            return self.errors


class DetailQuerySerializer(serializers.ModelSerializer):
    features =   FeatureCreateSerializer()  
    class Meta:
        model = OfferDetail
        fields = ['id', 'title','revisions','delivery_time_in_days','price','features','offer_type', ]

class SingleOfferGetSerializer(serializers.ModelSerializer):
    user_details = GetUserOffersSerializer(source='user', read_only=True)
    details = DetailQuerySerializer(many=True)
    class Meta:
        model = Offer
        fields = ['id', 'user','title', 'image', 'description', 'created_at', 'updated_at',  'details', 'min_price', 'min_delivery_time', 'user_details']

class SingleOfferPatchSerializer(serializers.ModelSerializer):
    details = DetailQuerySerializer(many=True)
    class Meta:
        model = Offer
        fields = ['id', 'user','title', 'image', 'description', 'created_at', 'updated_at',  'details', 'min_price', 'min_delivery_time',]
    
   
    def update(self, instance, validated_data):        
        try:
            details_val = validated_data.pop('details')
            if len(details_val) > 0:
                details_queryset = OfferDetail.objects.filter(offer=instance)
                for detail_val in details_val:
                    features_val = detail_val.pop('features')
                    detail_obj = details_queryset.get(offer_type=detail_val['offer_type'])
                    if detail_val['title']:
                        detail_obj.title = detail_val['title']
                    if detail_val['revisions']:
                        detail_obj.revisions = detail_val['revisions']
                    if detail_val['delivery_time_in_days']:
                        detail_obj.delivery_time_in_days = detail_val['delivery_time_in_days']
                    if detail_val['price']:
                        detail_obj.price = detail_val['price']

                    # remove all detail_feature relations and add new
                    detail_obj.features.clear()

                    for feature_val in features_val:
                        feature, created = Feature.objects.get_or_create(title=feature_val)
                    
                        detail_obj.features.add(feature)
                    detail_obj.save()
        except:
            pass

        instance.image = validated_data.get('image', instance.image)
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)

        instance.updated_at = timezone.now()
        instance.save()
        return instance

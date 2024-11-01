from rest_framework import serializers

from offer.api.serializers import DetailCreateSerializer, DetailSerializer, OfferGetSerializer
from offer.models import Detail, Feature, OfferDetail
from order.models import Order
from userprofile.models import UserProfile






class OrderSerializer(serializers.ModelSerializer):
    offer_detail = DetailCreateSerializer(read_only=True)

    offer_detail_id = serializers.PrimaryKeyRelatedField(
        queryset = OfferDetail.objects.all(),
        write_only=True,
        source = 'offer_detail'
    )

    class Meta:
        model = Order
        fields = '__all__'

   

    def create(self, validated_data):
        return Order.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    
    def validate_offer_detail_id(self, value):
        print(value)
        return value
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer_user = representation.pop('customer_user')
        business_user = representation.pop('business_user')
        status = representation.pop('status')

        representation['id'] = instance.id
        representation['customer_user'] = customer_user
        representation['business_user'] = business_user
        
        details = representation.pop('offer_detail')
        
        for key, value in details.items():
            if key is not 'id':
                representation[key] = value
        
        representation['status'] = status
        return representation
  
    
   

class OrderSetSerializer(serializers.Serializer):
    offer_detail = DetailCreateSerializer(read_only=True)
    offer_detail_id = serializers.PrimaryKeyRelatedField(
    queryset = OfferDetail.objects.all(),
    write_only=True,
    source='offer_detail'
    )

    customer_user = serializers.StringRelatedField()
    business_user = serializers.StringRelatedField()
    status = serializers.CharField(max_length=30, default='in_progress')
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer_user = representation.pop('customer_user')
        business_user = representation.pop('business_user')
        status = representation.pop('status')

        representation['id'] = instance.id
        representation['customer_user'] = customer_user
        representation['business_user'] = business_user
        
        details = representation.pop('offer_detail')
        
        for key, value in details.items():
            if key is not 'id':
                representation[key] = value
        
        representation['status'] = status
        return representation
  

    def create(self, validated_data):
        detail = validated_data.pop('offer_detail')
        details = OfferDetail.objects.get(pk=detail)

        order = Order(business_user=details.offer.user,
                    offer_detail=details,
                    **validated_data,
                    created_at=details.offer.created_at,
                    updated_at=details.offer.updated_at
                    )

        order.save() 
        
        return order

import re
from rest_framework import serializers
from offer.api.serializers import DetailCreateSerializer
from offer.models import Feature, OfferDetail
from order.models import Order


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
        """
        The patch request changes the status of the order
        """
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    
    def to_representation(self, instance):
        """
        Changes the representation of the Order.
        Change the name of the offer_detail to details and remove the id of the fields
        """
        representation = super().to_representation(instance)
        customer_user = representation.pop('customer_user')
        business_user = representation.pop('business_user')
        status = representation.pop('status')
        representation['id'] = instance.id
        representation['customer_user'] = customer_user
        representation['business_user'] = business_user
        details = representation.pop('offer_detail')
        
        for key, value in details.items():
            if key != 'id':
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
        """
        Change the representation of the fields.
        Changes the full customer user and business user to their ids.
        Change the name of offer_details to details and removes the id
        """
        representation = super().to_representation(instance)
        customer_user = representation.pop('customer_user')
        business_user = representation.pop('business_user')
        status = representation.pop('status')
        representation['id'] = instance.id
        representation['customer_user'] = int(re.search(r'\((.*?)\)',customer_user).group(1))
        representation['business_user'] = int(re.search(r'\((.*?)\)',business_user).group(1))
        details = representation.pop('offer_detail')
        
        for key, value in details.items():
            if key != 'id':
                representation[key] = value
        
        representation['status'] = status
        return representation
  

    def create(self, validated_data):
        """
        Create a new order with the given id of offer_detail if its existing
        """
        try:
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
        except:
            return self.errors

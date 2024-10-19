from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from offer.models import OfferDetail
from order.api.serializers import OrderSerializer, OrderSetSerializer
from order.models import Order
from userprofile.models import UserProfile


class OrderView(APIView):
    def get(self, request):
        offer = Order.objects.all()
        serializer = OrderSerializer(offer, many=True, )
        # context={'request': request}
        return Response(serializer.data)
    
    def post(self, request):
        customer_user = UserProfile.objects.get(user=request.user)
        print(customer_user)
        serializer = OrderSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer_user=customer_user)
            return Response(serializer.data)
        return Response(serializer.errors)
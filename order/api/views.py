from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from order.api.permissions import IsCustomerToPostOrder
from order.api.serializers import OrderSerializer, OrderSetSerializer
from order.models import Order
from userprofile.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist



class OrderView(APIView):
    
    permission_classes = [IsCustomerToPostOrder]
    def get(self, request):
        order = Order.objects.all()
        self.check_object_permissions(request, order)
        serializer = OrderSerializer(order, many=True, )
        # context={'request': request}
        return Response(serializer.data)
    
    def post(self, request):
        customer_user = UserProfile.objects.get(user=request.user)
        self.check_object_permissions(request, customer_user)
        serializer = OrderSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer_user=customer_user)
            return Response(serializer.data)
        return Response(serializer.errors)
    
class SingleOrderView(APIView):
    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def patch(self, request,pk):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        order_instance = Order.objects.get(pk=pk)
        order_instance.delete()
        return Response({})
    
class OrderCountView(APIView):
    def get(self, request, pk):
        try:
            user = UserProfile.objects.get(user=pk)
            if not user.type == 'business':
                return Response({"error": "Business user not found."})
            
            orders = Order.objects.filter(business_user=user)
            return Response({"order-count": len(orders)})
        except ObjectDoesNotExist:
            return Response({"error": "Business user not found."})
        
class CompetedOrderCountView(APIView):
    def get(self, request, pk):
        try:
            user = UserProfile.objects.get(user=pk)

            if not user.type == 'business':
                return Response({"error": "Business user not found."})
            
            orders = Order.objects.filter(business_user=user)
            completed = orders.filter(status='in_progress')
            return Response({"completed_order_count": len(completed)})
        
        except ObjectDoesNotExist:
            return Response({"error": "Business user not found."})
            
        

        


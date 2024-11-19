from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from order.api.permissions import IsBusinessUserOrAdmin, IsCustomerToPostOrder
from order.api.serializers import OrderSerializer, OrderSetSerializer
from order.models import Order
from userprofile.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404




class OrderView(APIView):
    
    permission_classes = [IsCustomerToPostOrder]
    def get(self, request):
        
        try:
            user = UserProfile.objects.get(user=request.user)
            order = Order.objects.all()
            if user.type == 'business':
                print(user.type)
                order = order.filter(business_user=user)
            else:
                print(user.type)
                order = order.filter(customer_user=user)            
        except:
            order = Order.objects.none()
        self.check_object_permissions(request, order)
        serializer = OrderSerializer(order, many=True, )
        return Response(serializer.data)
        
    
    def post(self, request):
        try:
            customer_user = UserProfile.objects.get(user=request.user)
            print(customer_user)
            self.check_object_permissions(request, customer_user)
        except:
            self.permission_denied(request)
        serializer = OrderSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer_user=customer_user)
            return Response(serializer.data)
        return Response(serializer.errors)
    
class SingleOrderView(APIView):
    permission_classes = [IsBusinessUserOrAdmin]
    def get(self, request, pk):
        try:
            order = get_object_or_404(Order, pk=pk)
        except:
            order = Order.objects.none()
        self.check_object_permissions(request, order)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def patch(self, request,pk):
        order = Order.objects.get(pk=pk)
        self.check_object_permissions(request, order)
        serializer = OrderSerializer(order, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        order_instance = Order.objects.get(pk=pk)
        self.check_object_permissions(request, order_instance)
        order_instance.delete()
        return Response({})
    
class OrderCountView(APIView):
    def get(self, request, pk):
        try:
            user = UserProfile.objects.get(user=pk)
            if not user.type == 'business':
                return Response({"error": "Business user not found."})
            
            orders = Order.objects.filter(business_user=user)
            orders = orders.filter(status='in_progress')
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
            completed = orders.filter(status='completed')
            return Response({"completed_order_count": len(completed)})
        
        except ObjectDoesNotExist:
            return Response({"error": "Business user not found."})
            
        

        


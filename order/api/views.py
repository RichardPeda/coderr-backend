from rest_framework.views import APIView
from rest_framework.response import Response
from order.api.permissions import IsBusinessUserOrAdmin, IsCustomerToPostOrder
from order.api.serializers import OrderSerializer, OrderSetSerializer
from order.models import Order
from userprofile.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


class OrderView(APIView):
    
    permission_classes = [IsCustomerToPostOrder]
    def get(self, request):
        """
        This endpoint returns a list of orders created either by the user as a customer or as a business partner.

        Args:
            request (user): Only orders created by the logged-in user either as a customer or as a business partner are returned.

        Returns:
            JSON: Serialized and filterd orders
        """
        
        try:
            user = UserProfile.objects.get(user=request.user)
            order = Order.objects.all()
            if user.type == 'business':
                order = order.filter(business_user=user)
            else:
                order = order.filter(customer_user=user)            
        except:
            order = Order.objects.none()
        self.check_object_permissions(request, order)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
        
    
    def post(self, request):
        """
        Create a new order based on the details of an offer (OfferDetail).
        

        Args:
            request (user, data): Only users with a CustomerProfile can create orders.
            The user specifies an OfferDetail ID and the order is created based on this offer.

        Returns:
            JSON: When the new order is created the serialized order will be returned, otherwise an error 
        """
        try:
            customer_user = UserProfile.objects.get(user=request.user)
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
        """
        Retrieve the details of a specific order using the ID.

        Args:
            request (auth.user): Authorized user.
            pk (_type_): primary key of the specific order.

        Returns:
            JSON: Serialized order if exists, otherwise empty.
        """
        try:
            order = get_object_or_404(Order, pk=pk)
        except:
            order = Order.objects.none()
        self.check_object_permissions(request, order)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def patch(self, request,pk):
        """
        Updating the status of an order (e.g. from “in_progress” to “completed” or “canceled”).

        Args:
            request (auth.user, data): Only the owner can update the order.
            pk (int): The ID of the order to be updated.

        Returns:
            JSON: Serialized updated order or error.
        """
        order = Order.objects.get(pk=pk)
        self.check_object_permissions(request, order)
        serializer = OrderSerializer(order, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        """
        Delete a specific order. 

        Args:
            request (auth.user): Only admin users (staff) may delete orders.
            pk (int): The ID of the order to delete.

        Returns:
            JSON: empty JSON
        """
        order_instance = Order.objects.get(pk=pk)
        self.check_object_permissions(request, order_instance)
        order_instance.delete()
        return Response({})
    
class OrderCountView(APIView):
    def get(self, request, pk):
        """
        This endpoint returns the number of orders in progress for a specific business user.
        Current orders are those with the status in_progress.

        Args:
            pk (_type_): Primary key of a specific user.

        Returns:
            JSON: If successfull the order count will be returned. Otherwise an error will be returned.
        """
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
        """
        Returns the number of completed orders for a specific business user.
        Completed orders have the status completed.

        Args:
            pk (int): Primary key of a specific user.

        Returns:
            JSON: If successfull the order count will be returned. Otherwise an error will be returned.
        """
        try:
            user = UserProfile.objects.get(user=pk)
            if not user.type == 'business':
                return Response({"error": "Business user not found."})
            orders = Order.objects.filter(business_user=user)
            completed = orders.filter(status='completed')
            return Response({"completed_order_count": len(completed)})
        except ObjectDoesNotExist:
            return Response({"error": "Business user not found."})
            
        

        


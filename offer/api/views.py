import re
from rest_framework.views import APIView
from rest_framework.response import Response

from offer.api.serializers import OfferGetSerializer, OfferCreateSerializer, DetailSerializer, SingleOfferGetSerializer, SingleOfferPatchSerializer
from offer.models import Offer, OfferDetail
from offer.api.permissions import IsBusinessUserToCreateOffer, IsOwnerOfOfferOrAdmin
from userprofile.models import Review, UserProfile
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters





class LargeResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 10000
    
class OfferFilter(filters.FilterSet):
    business_user_id = filters.NumberFilter(field_name='business_user')
    reviewer_id = filters.NumberFilter()
    class Meta:
        model = Review
        fields = ['business_user_id', 'reviewer_id']

class OfferView(APIView):
   
    serializer_class = OfferGetSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsBusinessUserToCreateOffer]
    
    def get(self, request):
        """
        This endpoint returns a list of offers.
        Each offer contains an overview of the offer details, the minimum price and the shortest delivery time.
        Query parameter:
        "creator_id": Filters the offers according to the user who created them.
        "min_price": Filters offers with a minimum price.
        "max_delivery_time": Filters offers whose delivery time is shorter than or equal to the specified value.
        "ordering": Sorts the offers according to the fields “updated_at” or “min_price”.
        "search": Searches the fields “title” and “description” for matches.
        "page_size": Specifies how many results should be returned per page. This is defined in the frontend in config.js, please set the page_size in your pagination to exactly the same value. This query parameter is not used directly.

        Args:
            request (auth.user): GET-Method allows any request

        Returns:
            JSON: The response is paginated according to PageNumberPagination. Returns a list of offers
        """
        queryset = Offer.objects.all()
        self.check_object_permissions(request, queryset)
        order_param = self.request.query_params.get('ordering', None)
        if order_param is not None and order_param != '':
            queryset = queryset.order_by(order_param)
        
        creator_id_param = self.request.query_params.get('creator_id', None)
        if creator_id_param is not None and creator_id_param  != '':
            queryset = queryset.filter(user=creator_id_param)

        min_price_param = self.request.query_params.get('min_price', None)
        if min_price_param is not None and min_price_param  != '':
            queryset = queryset.filter(min_price=min_price_param)

        max_delivery_time_param = self.request.query_params.get('max_delivery_time', None)
        if max_delivery_time_param is not None and max_delivery_time_param  != '':
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time_param)
            
        search_param = self.request.query_params.get('search', None)
        if search_param is not None and search_param != '':
            queryset = queryset.filter(Q(title__icontains=search_param) | Q(description__icontains=search_param))
            
        pagination_class = LargeResultsSetPagination
        paginator = pagination_class()
        
        page_param = self.request.query_params.get('page_size', None)
        if page_param is not None and search_param != '':
            page_size = re.sub('[/]', ' ', page_param)
            paginator.page_size= int(page_size)
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.serializer_class(page, many=True, context={'request': request})
        
        return paginator.get_paginated_response(serializer.data)
    
    
    @extend_schema(responses=OfferCreateSerializer)
    def post(self, request):
        """
        This endpoint makes it possible to create a new offer that must contain exactly three offer details (OfferDetail).
        These details should cover the basic, standard and premium types.
        Validation: 
        When creating an offer, exactly three details must be specified (and also the “offer_type” once each: basic, standard, premium). 
        In addition, everything should be present except an “image”. 
        The “revisions” are integers and start at -1 (the -1 is the “infinite revisions” case).
        The “delivery_time_in_days” are only positive integers.
        There should be at least one feature.

        Args:
            request (user, data): Only users who are also business users can create offers

        Returns:
            JSON: Serialized offer when successfull, otherwise an error.
        """
        business_user = UserProfile.objects.get(user=request.user)
        self.check_object_permissions(request, business_user)
        serializer = OfferCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=business_user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)


class SingleOfferView(APIView):
    permission_classes = [IsOwnerOfOfferOrAdmin]
    serializer_class = SingleOfferGetSerializer
    
    @extend_schema(responses=SingleOfferGetSerializer)
    def get(self, request, pk):
        """
        This endpoint returns a specific offer with the given primary key.
        
        Args:
            request (user): Authenticated user.
            pk (int): primary key of a specific offer.

        Returns:
            JSON: Serialized offer.
        """
        
        try:
            offer_detail = Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, offer_detail)
        serializer = self.serializer_class(offer_detail, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(responses=SingleOfferPatchSerializer)
    def patch(self, request, pk):
        """
        Updates a specific offer. A PATCH only overwrites the specified fields.

        Args:
            request (user, data): Only users who are authenticated and owner of the offer (or admin) can edit. 
            pk (int): primary key of a specific offer

        Returns:
            JSON: Serialized updated offer or error when data are invalid.
        """
        try:
            offer = Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        self.check_object_permissions(request, offer)
        serializer = SingleOfferPatchSerializer(offer, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        """
        Deletes a specific offer

        Args:
            request (_type_): Only users who are authenticated and owner of the offer (or admin) can delete. 
            pk (int): primary key of the specific offer

        Returns:
            JSON: Empty JSON
        """
        try:
            offer_instance = Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, offer_instance)
        offer_instance.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
  

class OfferDetailsView(APIView):
    serializer_class = DetailSerializer
    permission_classes = [IsOwnerOfOfferOrAdmin]

    # @swagger_auto_schema(request_body=DetailSerializer)
    def get(self, request, pk):
        """
        Retrieves the details of a specific offer detail.
        Args:
            request (user): Authenticated user. 
            pk (int): primary key of the specific offer detail.

        Returns:
            JSON: Serialized offer detail.
       
        """
        try:
            offer_detail = OfferDetail.objects.get(pk=pk)
        except OfferDetail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, offer_detail)
        serializer = self.serializer_class(offer_detail, context={'request': request})
        return Response(serializer.data)
    

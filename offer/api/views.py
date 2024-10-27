from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from offer.api.serializers import OfferDetailUrlSerializer, OfferGetSerializer, OfferCreateSerializer, DetailSerializer, SingleOfferGetSerializer, SingleOfferPatchSerializer
from offer.models import Offer, OfferDetail
from userprofile.models import UserProfile
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q



class LargeResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 10000


class OfferView(APIView):
  

    
    serializer_class = OfferGetSerializer
    pagination_class = LargeResultsSetPagination
        
    
    def get(self, request):
        queryset = Offer.objects.all()
        
        order_param = self.request.query_params.get('ordering', None)
        if order_param is not None and order_param is not '':
            queryset = queryset.order_by(order_param)
        
        # creator_id_param = self.request.query_params.get('creator_id', None)
        # if creator_id_param is not None and creator_id_param is not '':
        #     queryset = queryset.filter(user=creator_id_param)

        min_price_param = self.request.query_params.get('min_price', None)
        if min_price_param is not None and min_price_param is not '':
            queryset = queryset.filter(min_price=min_price_param)

        max_delivery_time_param = self.request.query_params.get('max_delivery_time', None)
        if max_delivery_time_param is not None and max_delivery_time_param is not '':
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time_param)
            
        search_param = self.request.query_params.get('search', None)
        if search_param is not None and search_param is not '':
            queryset = queryset.filter(Q(title__icontains=search_param) | Q(description__icontains=search_param))
            

        

        pagination_class = LargeResultsSetPagination
        paginator = pagination_class()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.serializer_class(page, many=True, context={'request': request})
        
        
        # serializer = self.serializer_class(offer, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
        # return Response(serializer.data)
    
    
    
    def post(self, request):

        business_user = UserProfile.objects.get(user=request.user)

        serializer = OfferCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=business_user)
            return Response(serializer.data)
        return Response(serializer.errors)

class SingleOfferView(APIView):
   
    def get(self, request,pk):
        offer_detail = Offer.objects.get(pk=pk)
        serializer = SingleOfferGetSerializer(offer_detail, context={'request': request})
        return Response(serializer.data)
    
    def patch(self, request,pk):
        offer = Offer.objects.get(pk=pk)
        serializer = SingleOfferPatchSerializer(offer, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
    
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        offer_instance = Offer.objects.get(pk=pk)
        offer_instance.delete()
        return Response({})
  


class OfferDetailsView(APIView):
    serializer_class = DetailSerializer

    def get(self, request,pk):

        offer_detail = OfferDetail.objects.get(pk=pk)
        print(offer_detail)
        serializer = self.serializer_class(offer_detail, context={'request': request})
     
        return Response(serializer.data)
    

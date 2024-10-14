from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from offer.api.serializers import OfferDetailUrlSerializer, OfferGetSerializer, OfferCreateSerializer, DetailSerializer, SingleOfferGetSerializer, SingleOfferPatchSerializer
from offer.models import Offer, OfferDetail
from django.db.models import Prefetch



class OfferView(APIView):

    def get(self, request):
        offer = Offer.objects.all()
        serializer = OfferGetSerializer(offer, many=True, context={'request': request})
     
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OfferCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors)
    


class SingleOfferView(APIView):
   

    def get(self, request,pk):
        offer_detail = Offer.objects.get(pk=pk)
        serializer = SingleOfferGetSerializer(offer_detail, context={'request': request})
        return Response(serializer.data)
    
    def patch(self, request,pk):
        queryset = Offer.objects.get(pk=pk)
        # queryset = Offer.objects.filter(pk=pk).prefetch_related(Prefetch('details', queryset=Detail.objects.all()))
        serializer = SingleOfferPatchSerializer(queryset, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
    
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        offer_instance = Offer.objects.get(pk=pk)
        offer_instance.delete()
        return Response({})
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.prefetch_related(
    #         Prefetch('post_set', queryset=Detail.objects.get(pk=280))
    #     )


class OfferDetailsView(APIView):
    serializer_class = DetailSerializer

    def get(self, request,pk):

        offer_detail = OfferDetail.objects.get(pk=pk)
        print(offer_detail)
        serializer = self.serializer_class(offer_detail, context={'request': request})
     
        return Response(serializer.data)
    

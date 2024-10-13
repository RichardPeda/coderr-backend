from rest_framework.views import APIView
from rest_framework.response import Response

from offer.api.serializers import OfferDetailUrlSerializer, OfferGetSerializer, OfferCreateSerializer, DetailSerializer, SingleOfferGetSerializer, SingleOfferPatchSerializer
from offer.models import Offer, Detail



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
        offer_detail = Offer.objects.get(pk=pk)
        print(f"offer_detail{offer_detail}")
        serializer = SingleOfferPatchSerializer(offer_detail, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        return Response(serializer.errors)



class OfferDetailsView(APIView):
    serializer_class = DetailSerializer

    def get(self, request,pk):

        offer_detail = Detail.objects.get(pk=pk)
        print(offer_detail)
        serializer = self.serializer_class(offer_detail, context={'request': request})
     
        return Response(serializer.data)
    

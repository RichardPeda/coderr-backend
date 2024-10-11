from rest_framework.views import APIView
from rest_framework.response import Response

from offer.api.serializers import OfferDetailUrlSerializer, OfferGetSerializer, OfferCreateSerializer, DetailSerializer
from offer.models import Offer, Detail



class OfferView(APIView):
    serializer_class = OfferGetSerializer

    def get(self, request):
        offer = Offer.objects.all()
        serializer = OfferGetSerializer(offer, many=True, context={'request': request})
     
        return Response(serializer.data)
    
    def post(self, request):
        serializer = OfferCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            print(f"serializer.data{serializer.data}")
            return Response(serializer.data)
        return Response(serializer.errors)
    


    # def perform_create(self, serializer):
      
    #     serializer.save(user=self.request.user)



# class OfferDetailView(APIView):
#     serializer_class = OfferDetailSerializer

#     def get(self, request):
#         offer_detail = OfferDetails.objects.all()
#         serializer = self.serializer_class(offer_detail, many=True, )
     
#         return Response(serializer.data)
    

class OfferDetailsView(APIView):
    serializer_class = DetailSerializer

    def get(self, request,pk):

        offer_detail = Detail.objects.get(pk=pk)
        print(offer_detail)
        serializer = self.serializer_class(offer_detail, context={'request': request})
     
        return Response(serializer.data)
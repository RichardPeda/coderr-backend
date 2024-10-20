from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from offer.api.serializers import DetailQuerySerializer
from offer.models import OfferDetail
from order.api.serializers import OrderSerializer, OrderSetSerializer
from order.models import Order
from userprofile.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist


class BaseInfoView(APIView):
    def get(self, request):
        queryset = OfferDetail.objects.all()


        review_count = 0
        for detail in queryset:
            review_count += detail.revisions

        average_rating = 0

        # print(revisions)
        # serializer = DetailQuerySerializer(revisions, many=True)
        return Response({})
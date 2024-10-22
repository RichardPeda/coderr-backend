from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from offer.api.serializers import DetailQuerySerializer
from offer.models import Offer, OfferDetail
from order.api.serializers import OrderSerializer, OrderSetSerializer
from order.models import Order
from userprofile.api.serializers import ReviewSerializer, UserProfileSerializer, UserSerializer
from userprofile.models import Review, UserProfile
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User




class BaseInfoView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        offers = Offer.objects.all()
        profiles= UserProfile.objects.filter(type='business')
        average_rating = 0
        for review in reviews:
            average_rating += review.rating
        average_rating = average_rating/len(reviews)
        return Response({
            "review_count": len(reviews),
            "average_rating": average_rating,
            "business_profile_count": len(profiles),
            "offer_count": len(offers),
            }
        )
    

class ReviewView(APIView):
    def get(self, request):
        queryset = Review.objects.all()

        business_user_id_param = self.request.query_params.get('business_user_id')
        if business_user_id_param is not None:
            queryset = queryset.filter(business_user=business_user_id_param)

        reviewer_id_param = self.request.query_params.get('reviewer_id')
        if reviewer_id_param is not None:
            queryset = queryset.filter(reviewer=reviewer_id_param)

        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)
    

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        *This function handles a post request for login of a registerd user.*
        *A post request returns a token, user id, email and name when the user exists.*
        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user.username)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username' : user.username
        })

class RegisterView(APIView):
    def post(self, request):
        """
        A GET-request return the html of the register page.
        A POST-request compares the given passwords and creates a new user.
        The function returns a JSON when is was successfull.
        """
        passwort_1 = request.data['password']
        passwort_2 = request.data['repeated_password']
        if passwort_1 == passwort_2:
            user = User.objects.create_user(username=request.data['username'], password=passwort_1, email=request.data['email'])
            serializer = UserSerializer(user)
        
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class SingleProfileView(APIView):
    def get(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        profile = UserProfile.objects.get(pk=pk)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class BusinessProfileView(APIView):
    def get(self, request):
        profiles = UserProfile.objects.filter(type='business')
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
class CustomerProfileView(APIView):
    def get(self, request):
        profiles = UserProfile.objects.filter(type='customer')
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)


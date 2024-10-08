from django.urls import path

from offer.api.views import OfferView


urlpatterns = [
    path('', OfferView.as_view(), name='offer'),
]
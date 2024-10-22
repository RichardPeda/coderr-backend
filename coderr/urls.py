"""
URL configuration for coderr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from offer.api.views import OfferView,OfferDetailsView, SingleOfferView
from order.api.views import CompetedOrderCountView, OrderCountView, OrderView, SingleOrderView
from userprofile.api.views import BaseInfoView, CustomerProfileView, LoginView, SingleProfileView, BusinessProfileView, RegisterView, ReviewView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view()),
    path('api/registration/', RegisterView.as_view()),
    path('api/profile/<int:pk>/', SingleProfileView.as_view()),  
    path('profiles/business/', BusinessProfileView.as_view()),  
    path('profiles/customer/', CustomerProfileView.as_view()),  



    path('offers/', OfferView.as_view()),
    path('offers/<int:pk>/', SingleOfferView.as_view()),
    path('offersdetails/<int:pk>/', OfferDetailsView.as_view(), name='offerdetail-detail'),


    path('orders/', OrderView.as_view()),
    path('orders/<int:pk>/', SingleOrderView.as_view()),
    path('order-count/<int:pk>/', OrderCountView.as_view()),
    path('completed-order-count/<int:pk>/', CompetedOrderCountView.as_view()),


    path('api/base-info/', BaseInfoView.as_view()),
    path('api/reviews/', ReviewView.as_view()),



]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
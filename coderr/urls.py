from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from offer.api.views import OfferView,OfferDetailsView, SingleOfferView
from order.api.views import CompetedOrderCountView, OrderCountView, OrderView, SingleOrderView
from userprofile.api.views import BaseInfoView, CustomerProfileView, LoginView, SingleProfileView, BusinessProfileView, RegisterView, ReviewView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView






urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/registration/', RegisterView.as_view(), name='registration'),
    path('api/profile/<int:pk>/', SingleProfileView.as_view(), name='singleprofile'),  
    path('api/profiles/business/', BusinessProfileView.as_view(), name='businessprofile'),  
    path('api/profiles/customer/', CustomerProfileView.as_view(), name='customerprofile'),  

    path('api/offers/', OfferView.as_view(), name='offers'),
    path('api/offers/<int:pk>/', SingleOfferView.as_view(), name='singleoffer'),
    path('api/offerdetails/<int:pk>/', OfferDetailsView.as_view(), name='offerdetail-detail'),

    path('api/orders/', OrderView.as_view(), name='orders'),
    path('api/orders/<int:pk>/', SingleOrderView.as_view(), name='singleorder'),
    path('api/order-count/<int:pk>/', OrderCountView.as_view(), name='order-count'),
    path('api/completed-order-count/<int:pk>/', CompetedOrderCountView.as_view(), name='completed-order-count'),

    path('api/base-info/', BaseInfoView.as_view(), name='base-info'),
    path('api/reviews/', ReviewView.as_view(), name='reviews'),
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
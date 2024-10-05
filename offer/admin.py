from django.contrib import admin

from offer.models import Features, Offer, OfferDetails

# Register your models here.
admin.site.register(Offer)
admin.site.register(OfferDetails)
admin.site.register(Features)
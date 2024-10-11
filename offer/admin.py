from django.contrib import admin

from offer.models import Feature, Offer, Detail

# Register your models here.
admin.site.register(Offer)
admin.site.register(Detail)
admin.site.register(Feature)
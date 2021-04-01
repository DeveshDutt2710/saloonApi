from django.contrib import admin
from .profiles.models import Profiles
from .products.models import Products
from .orders.models import Orders


admin.site.register(Profiles)
admin.site.register(Products)
admin.site.register(Orders)

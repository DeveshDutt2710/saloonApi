from django.contrib import admin
from .profiles.profile_service import Profiles
from  .products.product_service import Products


admin.site.register(Profiles)
admin.site.register(Products)

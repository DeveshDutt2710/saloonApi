from django.contrib import admin
from .profiles.models import Profiles
from  .products.models import Products


admin.site.register(Profiles)
admin.site.register(Products)

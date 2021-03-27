from django.urls import path, include

urlpatterns = [
    path('profiles/', include('admin_api.profiles.urls')),
    path('products/', include('admin_api.products.urls')),    
]

from djongo import models
from ..model_choices import *
from utility.exception_utilities import *
from utility.time_utilities import TimeUtilities
from djongo.models.fields import ObjectId
from ..profiles.profile_service import Profiles
from datetime import datetime
import json
from collections import OrderedDict  # don't remove this import
from rest_framework import serializers

class Products(models.Model):
    objects = models.DjongoManager()

    _id = models.ObjectIdField()
    name = models.TextField()
    description = models.TextField()
    price = models.IntegerField()

    sales = models.IntegerField(default=0)
    timings = models.JSONField()
    productAvailability = models.BooleanField(default=False)
    rating = models.IntegerField(default=5)

    productType = models.CharField(choices=PRODUCT_TYPES, max_length=1024, default=PRODUCT_TYPE_PRODUCT)
    vendorId = models.ForeignKey(Profiles, on_delete=models.CASCADE)

    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()

    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'products'

    @staticmethod
    def get_object_or_raise_exception(product_id):
        try:
            return Products.objects.get(pk=ObjectId(product_id))
        except Products.DoesNotExist:
            response = {
                'success': False,
                'detail': f'Product with id {product_id} does not exist'
            }
            raise InvalidProfileException(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_object_or_none(product_id):
        try:
            return Products.objects.get(pk=ObjectId(product_id))
        except Products.DoesNotExist:
            return None

    def delete_product(self):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):

        current_time = datetime.now()

        if not self.createdAt:
            self.createdAt = current_time

        self.updatedAt = current_time

        super(Products, self).save(*args, **kwargs)

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'

    def to_representation(self, profile):
        data = super(ProductSerializer, self).to_representation(profile)
        fields = self._readable_fields

        for field in fields:

            if field.field_name == "timings" and data[field.field_name] is not None:
                data[field.field_name] = dict(eval(data[field.field_name]))

            if data[field.field_name] is None:
                del data[field.field_name]

        return data

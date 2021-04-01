import json
from collections import OrderedDict  # don't remove this import
from rest_framework import serializers
from .models import Orders


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = '__all__'

    def to_representation(self, order):
        data = super(OrderSerializer, self).to_representation(order)
        fields = self._readable_fields

        json_fields = ['time', 'payment', 'contact']

        for field in fields:

            if field.field_name in json_fields and data[field.field_name] is not None:
                data[field.field_name] = dict(eval(data[field.field_name]))

            if data[field.field_name] is None:
                del data[field.field_name]

        return data
import json
from collections import OrderedDict  # don't remove this import
from rest_framework import serializers
from .models import Products


'''from bson import ObjectID
from bson.errors import InvalidID

class ObjectIdField(serializers.Field):
    """ Serializer field for Djongo ObjectID fields """
    def to_internal_value(self, data):
        # Serialized value -> Database value
        try:
            return ObjectId(str(data))  # Get the ID, then build an ObjectID instance using it
        except InvalidId:
            raise serializers.ValidationError(
                '`{}` is not a valid ObjectID'.format(data)

    def to_representation(self, value):
        # Database value -> Serialized value
        if not ObjectId.is_valid(value):  # User submitted ID's might not be properly structured
            raise InvalidId
        return smart_text(value)
'''


class ProductSerializer(serializers.ModelSerializer):
    #_id = ObjectIdField(read_only=True)

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

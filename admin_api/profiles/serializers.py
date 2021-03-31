import json
from bson import json_util
from collections import OrderedDict  # don't remove this import
from rest_framework import serializers
from .models import Profiles


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profiles
        fields = '__all__'

    def to_representation(self, profile):
        data = super(ProfileSerializer, self).to_representation(profile)
        fields = self._readable_fields

        json_fields = ['address', 'contact', 'privacySetting']

        for field in fields:

            if field.field_name == "myCoupons" and data[field.field_name] is not None:
                data[field.field_name] = json.loads(data[field.field_name])

            elif field.field_name in json_fields and data[field.field_name] is not None:
                data[field.field_name] = dict(eval(data[field.field_name]))

            if data[field.field_name] is None:
                del data[field.field_name]

        return data

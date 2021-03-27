import json
from bson import json_util
from collections import OrderedDict  # don't remove this import
from rest_framework import serializers
from djongo import models
from ..model_choices import *
from utility.exception_utilities import *
from utility.time_utilities import TimeUtilities
from djongo.models.fields import ObjectId
from datetime import datetime


class Profiles(models.Model):
    objects = models.DjongoManager()

    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    profileType = models.CharField(choices=PROFILE_TYPE, max_length=1024, default=PROFILE_TYPE_CUSTOMER)

    vendorDescription = models.TextField(null=True)
    contact = models.JSONField()

    address = models.JSONField()


    dob = models.DateTimeField()

    gender = models.CharField(max_length=10)
    image = models.TextField()

    lastAppActivity = models.DateTimeField(null=True)

    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()

    is_deleted = models.BooleanField(default=False)
    is_admin_verified = models.BooleanField(default=False)


    class Meta:
        managed = False
        db_table = 'profiles'

    @staticmethod
    def get_object_or_raise_exception(profile_id):
        try:
            return Profiles.objects.get(pk=ObjectId(profile_id))
        except Profiles.DoesNotExist:
            response = {
                'success': False,
                'detail': f'Profile with id {profile_id} does not exist'
            }
            raise InvalidProfileException(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_object_or_none(profile_id):
        try:
            return Profiles.objects.get(pk=ObjectId(profile_id))
        except Profiles.DoesNotExist:
            return None

    def delete_profile(self):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):

        current_time = datetime.now()

        if not self.createdAt:
            self.createdAt = current_time

        self.updatedAt = current_time

        super(Profiles, self).save(*args, **kwargs)
        return self._id
    
    def update(self, *args, **kwargs):

        self.updatedAt = datetime.now()
        print("TESTING")
        super(Profiles, self).update(*args, **kwargs)



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


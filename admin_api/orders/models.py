from djongo import models
from ..model_choices import *
from utility.exception_utilities import *
from utility.time_utilities import TimeUtilities
from djongo.models.fields import ObjectId
from datetime import datetime
from ..products.models import Products
from ..profiles.models import Profiles


class Orders(models.Model):
    objects = models.DjongoManager()

    _id = models.ObjectIdField()

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    print(type(productId))
    vendorId = models.ForeignKey(Profiles, on_delete=models.CASCADE)
    print(type(vendorId))
    customerId = models.TextField()
    customerName = models.TextField()

    contact = models.JSONField()

    payment = models.JSONField()

    time = models.JSONField()

    date = models.DateTimeField(auto_now_add=True)

    orderStatus = models.CharField(choices=ORDER_STATUS, max_length=1024, default=ORDER_STATUS_UPCOMING)

    createdAt = models.DateTimeField()
    updatedAt = models.DateTimeField()

    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'orders'

    @staticmethod
    def get_object_or_raise_exception(order_id):
        try:
            return Orders.objects.get(pk=ObjectId(order_id))
        except Orders.DoesNotExist:
            response = {
                'success': False,
                'detail': f'Order with id {order_id} does not exist'
            }
            raise InvalidProfileException(response, status_code=status_codes.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_object_or_none(order_id):
        try:
            return Orders.objects.get(pk=ObjectId(order_id))
        except Orders.DoesNotExist:
            return None

    def delete_order(self):
        self.is_deleted = True
        self.save()

    def save(self, *args, **kwargs):

        current_time = datetime.now()

        if not self.createdAt:
            self.createdAt = current_time

        self.updatedAt = current_time

        super(Orders, self).save(*args, **kwargs)

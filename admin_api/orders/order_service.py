from utility.pagination_utilities import PaginationUtilities
from .serializers import OrderSerializer
from ..serializers import BsonSerializer
from .models import Orders
from ..profiles.models import Profiles
from ..products.models import Products
from djongo.models.fields import ObjectId


class OrderService():

    order_id = None
    page = 1
    page_size = 10

    def __init__(self, order_id: str = None, page: int = 1, page_size: int = 10):
        self.set_order_id(order_id)
        self.page = page
        self.page_size = page_size

    def set_order_id(self, order_id):
        self.order_id = order_id

    def get_order_id(self):
        return self.order_id

    def fetch_all_orders(self) -> dict:
        orders = Orders.objects.all()  # .filter(is_deleted=False)

        orders = PaginationUtilities.paginate_results(orders,
                                                      page_number=self.page,
                                                      page_size=self.page_size)

        orders_data = OrderSerializer(orders, many=True)

        response = {
            'success': True,
            'orders': orders_data.data
        }

        return response

    def fetch_order_by_id(self) -> dict:
        order = Orders.get_object_or_raise_exception(self.get_order_id())

        order_data = OrderSerializer(order)

        response = {
            'success': True,
            'order': order_data.data
        }

        return response

    def create_order(self, data) -> dict:

        Orders(**data).save()

        response = {
            'success': True,
        }

        return response

    def update_order(self, data) -> dict:

        Orders.objects.filter(pk=ObjectId(self.get_order_id())).update(**data)

        response = {
            'success': True,
        }

        return response

    def delete_order(self) -> dict:
        order = Orders.get_object_or_raise_exception(self.get_order_id())

        order.delete_order()

        response = {
            'success': True,
        }

        return response

    def search_order(self, query) -> dict:

        orders = [i for i in Orders.objects.mongo_find(
            {'$or': [{'customerName': {"$regex": f'.*{query}.*', "$options": "i"}},
                     {'contact.email': {"$regex": f'.*{query}.*', "$options": "i"}},
                     {'contact.phone': {"$regex": f'.*{query}.*', "$options": "i"}}
                     ]
             }
        )]

        orders = PaginationUtilities.paginate_results(orders,
                                                      page_number=self.page,
                                                      page_size=self.page_size)

        data = BsonSerializer.serialize_search_results(orders)

        response = {
            'success': True,
            'orders': data
        }

        return response


class OrderUtilities:

    @staticmethod
    def fetch_product(product_id):
        return Products.get_object_or_raise_exception(product_id)

    @staticmethod
    def fetch_profile(profile_id):
        return Profiles.get_object_or_raise_exception(profile_id)

    @staticmethod
    def create_payment(payment_data):
        return Payments(**payment_data).save()

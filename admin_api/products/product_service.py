from utility.pagination_utilities import PaginationUtilities
from .serializers import ProductSerializer
from .models import Products
from ..serializers import BsonSerializer
from djongo.models.fields import ObjectId


class ProductService():

    product_id = None
    page = 1
    page_size = 10

    def __init__(self, product_id: str = None, page: int = 1, page_size: int = 10):
        self.set_product_id(product_id)
        self.page = page
        self.page_size = page_size

    def set_product_id(self, product_id):
        self.product_id = product_id

    def get_product_id(self):
        return self.product_id

    def fetch_all_products(self) -> dict:
        products = Products.objects.all()  # .filter(is_deleted=False)

        products = PaginationUtilities.paginate_results(products,
                                                        page_number=self.page,
                                                        page_size=self.page_size)

        data = ProductSerializer(products, many=True).data

        response = {
            'success': True,
            'products': data
        }

        return response

    def fetch_product_by_id(self) -> dict:
        product = Products.get_object_or_raise_exception(self.get_product_id())

        product_data = ProductSerializer(product)

        response = {
            'success': True,
            'product': product_data.data
        }

        return response

    def create_product(self, data) -> dict:

        Products(**data).save()

        response = {
            'success': True,
        }

        return response

    def update_product(self, data) -> dict:

        Products.objects.filter(pk=ObjectId(self.get_product_id())).update(**data)

        response = {
            'success': True,
        }

        return response

    def delete_product(self) -> dict:
        product = Products.get_object_or_raise_exception(self.get_product_id())

        product.delete_product()

        response = {
            'success': True,
        }

        return response

    def search_product(self, query):

        products = [i for i in Products.objects.mongo_find(
            {'$or': [{'name': {"$regex": f'.*{query}.*', "$options": "i"}}
                     ]
             }
        )]

        products = PaginationUtilities.paginate_results(products,
                                                        page_number=self.page,
                                                        page_size=self.page_size)

        data = BsonSerializer.serialize_search_results(products)

        response = {
            'success': True,
            'profiles': data
        }

        return response

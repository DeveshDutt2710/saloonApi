from utility.pagination_utilities import PaginationUtilities
from .profile_service import ProfileSerializer
from ..serializers import BsonSerializer
from .profile_service import Profiles
from djongo.models.fields import ObjectId
from datetime import datetime



class ProfileImpl():
    profile_id = None
    page = 1
    page_size = 10

    def __init__(self, profile_id: str = None, page: int = 1, page_size: int = 10):
        self.set_profile_id(profile_id)
        self.page = page
        self.page_size = page_size

    def set_profile_id(self, profile_id):
        self.profile_id = profile_id

    def get_profile_id(self):
        return self.profile_id

    def _replace_id_to_object_ids_for_user_coupons(self, userCoupons):
        for coupon in userCoupons:
            coupon['_id'] = ObjectId(coupon['_id'])

    def fetch_all_profiles(self) -> dict:
        profiles = Profiles.objects.all()  # .filter(is_deleted=False)

        profiles = PaginationUtilities.paginate_results(profiles,
                                                        page_number=self.page,
                                                        page_size=self.page_size)

        profile_data = ProfileSerializer(profiles, many=True)

        response = {
            'success': True,
            'profiles': profile_data.data
        }

        return response

    def fetch_profile_by_id(self) -> dict:
        profiles = Profiles.get_object_or_raise_exception(self.get_profile_id())

        profile_data = ProfileSerializer(profiles)

        response = {
            'success': True,
            'profile': profile_data.data
        }

        return response

    def create_profile(self, data) -> dict:
        #my_coupons = data.pop('myCoupons') if 'myCoupons' in data else []
        #self._replace_id_to_object_ids_for_user_coupons(my_coupons)
        #data['myCoupons'] = my_coupons

        data = Profiles(**data).save()

        response = {
            'success': True,
            'profile_id' : str(data)
        }

        return response

    def update_profile(self, data) -> dict:
        #my_coupons = data.pop('myCoupons') if 'myCoupons' in data else []
        #self._replace_id_to_object_ids_for_user_coupons(my_coupons)
        #data['myCoupons'] = my_coupons
        print(type(data))
        data['updatedAt'] = datetime.now()

        filtered_profile = Profiles.objects.filter(pk=ObjectId(self.get_profile_id()))
        filtered_profile.update(**data)

        response = {
            'success': True,
            'profile_id' : str(self.get_profile_id())
        }


        return response

    def delete_profile(self) -> dict:
        profile = Profiles.get_object_or_raise_exception(self.get_profile_id())

        profile.delete_profile()

        response = {
            'success': True,
        }

        return response

    def search_profile(self, query):
        profiles = [i for i in Profiles.objects.mongo_find(
            {'$or': [{'name': {"$regex": f'.*{query}.*', "$options": "i"}},
                     {'contact.email': {"$regex": f'.*{query}.*', "$options": "i"}},
                     {'contact.phone': {"$regex": f'.*{query}.*', "$options": "i"}}
                     ]
             }
        )]

        profiles = PaginationUtilities.paginate_results(profiles,
                                                        page_number=self.page,
                                                        page_size=self.page_size)

        data = BsonSerializer.serialize_search_results(profiles)

        response = {
            'success': True,
            'profiles': data
        }

        return response

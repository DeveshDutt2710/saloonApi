
from rest_framework.views import APIView
from rest_framework import status as status_codes
from django.http import JsonResponse
from .profile_service import Profiles
from .profile_impl import ProfileImpl


class allProfileView(APIView):
    def getAllProfile(request):
        query_params = request.query_params
        page_no = query_params.get('page', 1)
        page_size = query_params.get("page_size", 10)

        profile_manager = ProfileImpl(page=page_no, page_size=page_size)
        response = profile_manager.fetch_all_profiles()

        return response

class getProfileView(APIView):

    def getProfileById(profile_id):

        profile_manager = ProfileImpl(profile_id)
        response = profile_manager.fetch_profile_by_id()

        return response


class createProfileView(APIView):

    def createProfile(request):

        profile_manager = ProfileImpl()
        response = profile_manager.create_profile(request.data)

        return response


class updateProfileView(APIView):

    def updateProfile(request,profile_id):

        profile_manager = ProfileImpl(profile_id)
        response = profile_manager.update_profile(request.data)

        return response


class deleteProfileView(APIView):

    def deleteProfile(profile_id):

        profile_manager = ProfileImpl(profile_id)
        response = profile_manager.delete_profile()

        return response


class searchProfileView(APIView):

    def searchProfile(request, query):
        query_params = request.query_params

        page_no = query_params.get('page', 1)
        page_size = query_params.get("page_size", 10)

        profile_manager = ProfileImpl(page=page_no, page_size=page_size)
        response = profile_manager.search_profile(query)

        return response


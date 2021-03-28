from rest_framework.views import APIView
from rest_framework import status as status_codes
from django.http import JsonResponse
from .profile_service import Profiles
from .profile_impl import ProfileImpl
from .abstract import * 

class AllProfileView(APIView):

    def get(self, request, *args, **kwargs):

        response = allProfileView.getAllProfile(request)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class GetProfileView(APIView):

    def get(self, request, profile_id, *args, **kwargs):

        response = getProfileView.getProfileById(profile_id)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class CreateProfileView(APIView):

    def post(self, request, *args, **kwargs):

        response = createProfileView.createProfile(request)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class UpdateProfileView(APIView):

    def post(self, request, profile_id, *args, **kwargs):

        response = updateProfileView.updateProfile(request, profile_id)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class DeleteProfileView(APIView):

    def post(self, request, profile_id, *args, **kwargs):

        response = deleteProfileView.getAllProfile(profile_id)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class SearchProfileView(APIView):

    def post(self, request, query, *args, **kwargs):
        response = searchProfileView.getAllProfile(request, query)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)

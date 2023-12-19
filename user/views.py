from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from base.models import User
from .models import UserProfile
from .serializers import (
    UserProfileSerializer,
    UserProfileListSerializer,
    UsersSerializer,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import MultiPartParser, FormParser
import logging

logger = logging.getLogger(__name__)


# UserProfileView
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(
                {"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(user=request.user)
            user = User.objects.get(email=request.user)
            user.is_profile = True
            user.save()
        except UserProfile.DoesNotExist:
            return Response(
                {"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Updated successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# UserProfileListing
class UserProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profiles = UserProfile.objects.all()
        serializer = UserProfileListSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# # UserProfileDetails
# class AuthenticatedUserProfile(APIView):
#     permission_classes = [IsAuthenticated]


#     def get(self, request):
#         try:
#             profile = UserProfile.objects.get(user=request.user)
#             serializer = UserProfileListSerializer(profile)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except UserProfile.DoesNotExist:
#             return Response({'message': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
class UserProfileListCreateView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


# class UserProfileUpdateView(generics.UpdateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#     permission_classes = [IsAuthenticated]


#     def get_object(self):
#         return self.request.user.userprofile
class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]

    def patch(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        serializer = UserProfileSerializer(
            user_profile, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

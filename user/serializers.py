from rest_framework import serializers
from base.models import User
from servicer.serializers import ServicerSerializer
from events.models import Event
from base.serializers import UserSerializer
from .models import UserProfile


# User
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number','is_active']


# # UserProfile
# class UserProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = UserProfile
#         fields = '__all__'
        
        


# UserProfileListing
class UserProfileListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'profile_photo']  
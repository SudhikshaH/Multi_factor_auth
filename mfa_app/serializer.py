from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import UserDetails

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['id', 'name', 'email', 'password', 'token']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password isn't returned in responses
            'token': {'read_only': True},  # Token should not be writable
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
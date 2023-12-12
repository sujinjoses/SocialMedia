from rest_framework import serializers
#from django.contrib.auth.models import User
from accounts.models import User, Friend
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework.serializers import ValidationError


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        try:
            user = User.objects.create(
                email=validated_data['email'].lower(),
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name']
            )
        except IntegrityError:
            raise ValidationError('User information already exists.')
        
        user.set_password(validated_data['password'])
        user.save()

        return user
    

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('__all__')
        read_only_fields = ('id', 'requester', 'status_type')


class FriendAcceptRejectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = ('__all__')
        read_only_fields = ('id', 'requester', 'requestee')
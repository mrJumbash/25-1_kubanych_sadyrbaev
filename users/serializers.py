from django.contrib.auth.models import User
from .models import ConfirmCode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from random import randint, choice

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_password(self, password):
        '''CUSTOM VALIDATION METHOD'''
        return password
class UserLoginValidateSerializer(UserLoginSerializer):
    pass

class UserRegValidateSerializer(UserLoginSerializer):
    # confirm_code = serializers.CharField(required=False)
    # confirm_code_id = serializers.IntegerField(required=False)
    # confirm_code_id = serializers.ListField(child=serializers.IntegerField(), required=False)
    def validate_username(self, username):
        try:
            User.objects.get(username=username)

        except User.DoesNotExist:
            return username

        raise ValidationError('Already exists')


class UserConfirmValidateSerializer(UserLoginSerializer):

    class Meta:
        model = ConfirmCode
        fields = ['id', 'code']
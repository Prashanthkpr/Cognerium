from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from menu.base import CustomModelSerializers
from users.models import User


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get('username', "")
        password = data.get('password', "")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
        return data


class UserSerializer(CustomModelSerializers):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def get_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key

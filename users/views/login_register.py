from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from users.serializers import UserLoginSerializer, UserSerializer


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return render(
            request, 'users/login.html',
        )

    def post(self, request):
        login_serializer = UserLoginSerializer(data=request.data.get('login_data'))
        login_serializer.is_valid(raise_exception=True)
        user = login_serializer.validated_data.get('user')
        if user:
            login(request, user)
            user_serializer = UserSerializer(
                user, context={'data': {'fields': ['first_name', 'last_name', 'email', 'token']}}
            )
            return Response({'success': True, 'user': user_serializer.data})
        return Response({'success': False, 'error': "Unable to login with given credentials"})

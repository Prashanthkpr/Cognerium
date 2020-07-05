import datetime
from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
from blog.models import Blog
from menu.base import CustomPaginator
from blog.serializers import BlogSerializers
from users.serializers import UserSerializer


# Create your views here.


class BlogView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if request.GET.get('get_data'):
            blogs = Blog.objects.filter(
                Q(visible_to__in=['public', 'congerium']) &
                (Q(author=user))
            ).distinct().order_by('-published_at')
            no_of_feeds = blogs.count()
            page_number = request.GET.get('page_number') or 1
            page_size = request.GET.get('page_size') or 5
            blogs = CustomPaginator(
                blogs, page_size=page_size, page_number=page_number
            )
            for blog in blogs:
                if user not in blog.views.all() and blog.author.id != user.id:
                    blog.views.add(user)
            blog_serializers = BlogSerializers(
                blogs, many=True,
                context={'user': user}
            )
            user_data = UserSerializer(
                user,
                context={'data': {
                    'fields': [
                        'id', 'full_name', 'first_name', 'last_name',
                    ]}
                })
            return Response(
                {'success': True,
                 'blogs': blog_serializers.data,
                 'no_of_feeds': no_of_feeds,
                 'like_symbols': Blog.CLDR_CHOICES,
                 'user_data': user_data.data}
            )
        return render(request, 'blog/home.html')

    def post(self, request):
        text_data = request.data.get('text_data')
        if text_data:
            blog = Blog.objects.create(
                description=text_data,
                author=request.user,
                visible_to=request.data.get('blog_visible', 'jobways')
            )
            serializer = BlogSerializers(
                blog, context={'user': request.user}
            )
            return Response(
                {'success': True,
                 'blog': serializer.data,
                 }
            )
        return Response({
            'success': False,
            'error': "Insuffient data"
        })

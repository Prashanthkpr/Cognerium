from rest_framework import serializers
from blog.models import (
    Blog, LikeOnFeed, Comment, LikeOnComment, CommentOnComment, FeedAttachement,
)
from django.contrib.humanize.templatetags.humanize import *
from menu.base import CustomModelSerializers
from users.serializers import UserSerializer


# Blog Feed Serializers


class LikeOnCommentSerializers(CustomModelSerializers):
    author = UserSerializer(
        context={'data': {
            'fields': [
                'id', 'full_name',
                'first_name', 'last_name'
            ]}
        })

    class Meta:
        model = LikeOnComment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class CommentOnCommentSerializers(CustomModelSerializers):
    author = UserSerializer(
        context={'data': {
            'fields': [
                'id', 'full_name',
                'first_name', 'last_name'
            ]}
        })

    class Meta:
        model = CommentOnComment
        fields = "__all__"


class CommentSerializers(CustomModelSerializers):
    author = UserSerializer(
        context={'data': {
            'fields': [
                'id', 'full_name',
                'first_name', 'last_name'
            ]}
        })
    commentoncomment_set = CommentOnCommentSerializers(many=True)
    natural_time = serializers.SerializerMethodField()
    is_request_user_liked = serializers.SerializerMethodField()
    is_request_user_commented = serializers.SerializerMethodField()
    request_user_like_symbol = serializers.SerializerMethodField()
    no_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def get_liked_symbols(self, obj):
        if obj.likeoncomment_set.exists():
            return set(obj.likeoncomment_set.values_list('cldr', flat=True))

    def get_natural_time(self, obj):
        return naturaltime(obj.published_at)

    def get_is_request_user_liked(self, obj):
        user = self.context.get('user', None)
        if user:
            return obj.likeoncomment_set.filter(author=user).exists()
        return False

    def get_is_request_user_commented(self, obj):
        user = self.context.get('user', None)
        if user:
            return obj.commentoncomment_set.filter(author=user).exists()
        return False

    def get_request_user_like_symbol(self, obj):
        user = self.context.get('user', None)
        if user:
            like_obj = obj.likeoncomment_set.filter(author=user).first()
            if like_obj:
                return like_obj.cldr
            return None
        return None

    def get_no_of_likes(self, obj):
        return intcomma(obj.likeoncomment_set.count())


class LikeOnFeedSerializers(CustomModelSerializers):
    author = UserSerializer(
        context={'data': {
            'fields': [
                'id', 'full_name',
                'first_name', 'last_name'
            ]}
        })

    class Meta:
        model = LikeOnFeed
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class FeedAttachementSerializers(CustomModelSerializers):

    class Meta:
        model = FeedAttachement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class BlogSerializers(CustomModelSerializers):
    CLDR_CHOICES = {
        ':thumbs_up:': {'symbol': '👍', 'title': "Like"},
        ':handshake:': {'symbol': '🤝', 'title': "Congrats"},
        ':OK_hand:': {'symbol': '👌', 'title': "Awesome"},
        ':clapping_hands:': {'symbol': '👏', 'title': "Good Work"}
    }
    author = UserSerializer(
        context={'data': {
            'fields': [
                'id', 'full_name',
                'first_name', 'last_name'
            ]}
        })
    comment_set = serializers.SerializerMethodField()
    feedattachement_set = FeedAttachementSerializers(many=True)
    total_comments = serializers.SerializerMethodField()
    natural_time = serializers.SerializerMethodField()
    liked_symbols = serializers.SerializerMethodField()
    is_request_user_liked = serializers.SerializerMethodField()
    shares_count = serializers.SerializerMethodField()
    is_request_user_shared = serializers.SerializerMethodField()
    request_user_like_symbol = serializers.SerializerMethodField()
    no_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    def get_likes_symbol(self, obj):
        return self.CLDR_CHOICES

    def get_natural_time(self, obj):
        return naturaltime(obj.published_at)

    def get_liked_symbols(self, obj):
        if obj.likeonfeed_set.exists():
            return set(obj.likeonfeed_set.values_list('cldr', flat=True))
        return None

    def get_total_comments(self, obj):
        return obj.comment_set.count()

    def get_comment_set(self, obj):
        comments = CustomPaginator(
            obj.comment_set.all().order_by('-published_at'), page_size=2
        )
        return CommentSerializers(
            comments, many=True,
            context={'user': self.context.get('user')}
        ).data

    def get_is_request_user_liked(self, obj):
        user = self.context.get('user', None)
        if user:
            return obj.likeonfeed_set.filter(author=user).exists()
        return False

    def get_shares_count(self, obj):
        return obj.shares.count()

    def get_is_request_user_shared(self, obj):
        user = self.context.get('user', None)
        if user:
            return obj.shares.filter(author=user).exists()
        return False

    def get_request_user_like_symbol(self, obj):
        user = self.context.get('user', None)
        if user:
            like_obj = obj.likeonfeed_set.filter(author=user).first()
            if like_obj:
                return like_obj.cldr
            return None
        return None

    def get_no_of_likes(self, obj):
        return intcomma(obj.likeonfeed_set.count())

from django.db import models

# Create your models here.


class PublishInfo(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Attachment(models.Model):
    file_type = models.CharField(max_length=10, choices=(
        ('doc', 'Document'), ('image', 'Image',), ('video', 'Video'), ('audio', 'Audio')
    ))
    file_name = models.CharField(max_length=100, unique=True)
    url = models.URLField(max_length=600, blank=True, null=True, unique=True)

    class Meta:
        abstract = True


class Blog(PublishInfo):
    CLDR_CHOICES = {
        ':thumbs_up:': {'symbol': '👍', 'title': "Like"},
        ':handshake:': {'symbol': '🤝', 'title': "Congrats"},
        ':OK_hand:': {'symbol': '👌', 'title': "Awesome"},
        ':clapping_hands:': {'symbol': '👏', 'title': "Good Work"}
    }
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True)
    shares = models.ManyToManyField(
        'blog.Blog', blank=True
    )
    views = models.ManyToManyField(
        'users.User', blank=True,
        related_name='blog_views'
    )
    hidden_users = models.ManyToManyField(
        'users.User', blank=True,
        related_name='hidden_users'
    )
    visible_to = models.CharField(
        max_length=15, null=True,
        choices=(
            ('public', "Public"),
            ('congerium', " Network"),
            ('connections', "Congerium Connections"),
            ('private', "Private")
        ),
        default='congerium'
    )
    link = models.URLField(max_length=600, null=True, blank=True, unique=True)

    def __str__(self):
        return "%s - %s - %s" % (self.author, self.title, self.published_at)


class FeedAttachement(Attachment):
    feed = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s - %s" % (self.feed, self.file_type, self.file_name)


class Like(PublishInfo):
    CLDR_CHOICES = (
        (':thumbs_up:', '👍'),
        (':handshake:', '🤝'),
        (':OK_hand:', '👌'),
        (':clapping_hands:', '👏')
    )
    cldr = models.CharField(
        max_length=100, choices=CLDR_CHOICES)
    code = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        abstract = True


class LikeOnFeed(Like):
    feed = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return "%s- %s - %s" % (self.feed, self.author, self.cldr)


class Comment(PublishInfo):
    description = models.TextField(null=False)
    feed = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return "%s- %s - %s" % (self.feed, self.author, self.published_at)


class LikeOnComment(Like):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return "%s- %s - %s" % (self.comment, self.author, self.cldr)


class CommentOnComment(PublishInfo):
    description = models.TextField(null=False)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return "%s- %s - %s" % (self.comment, self.author, self.published_at)

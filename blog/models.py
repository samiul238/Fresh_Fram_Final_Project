from django.db import models
from django.contrib.auth.models import User
from base.models import Custom_User
# from base.views import printer


class Blog(models.Model):
    title = models.CharField(max_length=150)
    image = models.FileField(upload_to='blog/post/')
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    share = models.IntegerField(default=0)
    tags = models.CharField(max_length=50, blank=True, null=True)
    tag_list = models.CharField(max_length=50, blank=True, null=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.tags is not None and self.tags != '':
            self.tag_list = list(
                map(lambda x: x.strip(), self.tags.split(',')))
        else:
            self.tag_list = '["No Tags"]'
        super(Blog, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def user_avatar(self):
        cu = Custom_User.objects.get(user=self.user)
        return cu.avatar

    def comment_count(self):
        # printer('count_count')
        comments = Comment.objects.filter(blog=self)
        return len(comments)


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.blog.title)[0:50] + ' (' + str(self.user) + ') ' + ': ' + str(self.comment)[0:100]

    def user_avatar(self):
        cu = Custom_User.objects.get(user=self.user)
        return cu.avatar


class ReplyComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rep_comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.rep_comment)[0:50] + '...'

    def cu(self):
        cu = Custom_User.objects.get(user=self.user)
        return cu

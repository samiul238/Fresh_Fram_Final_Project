from django.db import models
from django.contrib.auth.models import User


class PaymentGatewaySettings(models.Model):

    store_id = models.CharField(max_length=500, blank=True, null=True)
    store_pass = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = "PaymentGatewaySetting"
        verbose_name_plural = "PaymentGatewaySettings"
        db_table = "paymentgatewaysettings"


class Home_Banner(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField(upload_to='home_banner', default='homebanner.jpg')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class Offer(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='offer')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    subject = models.CharField(max_length=100, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name + ': ' + self.subject


class Subscribe(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class Custom_User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.FileField(
        upload_to='profile/avatar/', default='default_profile320.png', blank=True, null=True)

    join_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField(blank=True, null=True, default='None')

    def __str__(self):
        return str(self.user)

    def delete(self, *args, **kwargs):
        self.avatar.delete()
        super().delete(*args, **kwargs)

    def get_avatar(self):
        try:
            avatar = self.avatar.url
            return avatar
        except:
            return '/media/default_profile320.png'


class Contact_Number(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_type = models.CharField(max_length=20, blank=True, null=True)
    number = models.CharField(max_length=20)

    def __str__(self):
        return str(self.user) + ': ' + self.number


class Brand(models.Model):
    name = models.CharField(max_length=30, unique=True)
    image = models.FileField(upload_to='brand/', default='brand.jpg')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

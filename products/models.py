from django.db import models
from django.contrib.auth.models import User
from base.models import Custom_User
from multiselectfield import MultiSelectField


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    image = models.FileField(upload_to='category', default='now')

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class Sub_Category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(
        Sub_Category, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=100)
    unit_choices = (
        ('kilo', 'kilo'),
        ('piece', 'piece')
    )
    unit = models.CharField(max_length=30, choices=unit_choices)
    image = models.FileField(upload_to='products/')

    product_id = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField()
    tags = models.CharField(max_length=100, blank=True, null=True)
    tag_list = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=30, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    views = models.IntegerField(default=0, blank=True, null=True)
    star_rating = models.CharField(max_length=20)
    count_in_stock = models.IntegerField(default=1)
    order_count = models.IntegerField(default=1)
    certificate = models.FileField(
        upload_to='products/', blank=True, null=True)

    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)

    discount_percent = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)

    include_choices = (
        ('new', 'new'),
        ('featured', 'featured'),
        ('sale', 'sale')
    )
    include = MultiSelectField(choices=include_choices, blank=True)
    video = models.FileField(
        upload_to='products/video/', default='product_video', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.tags is not None and self.tags != '':
            self.tag_list = list(
                map(lambda x: x.strip(), self.tags.split(',')))
        else:
            self.tag_list = '["No Tags"]'

        self.star_rating = self.rating()

        self.discount_percent = round(
            (100 / self.price) * (self.price - self.discount_price), 2)

        super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        self.video.delete()
        # self.certificate.delete()
        super().delete(*args, **kwargs)

    def rating(self):
        ratings = Rating.objects.filter(product=self)

        stars = 0
        for rating in ratings:
            stars += rating.star

        try:
            avg_rating = round(stars / len(ratings), 2)
        except ZeroDivisionError:
            avg_rating = 'Not rated'

        return avg_rating


class DeliveryAddress(models.Model):
    types = (
        ('Home', 'Home'),
        ('Office', 'Office'),
        ('Business', 'Business'),
    )
    address_type = models.CharField(max_length=15, choices=types)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.address_type + ': ' + self.address


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user) + ': ' + str(self.product) + ' (' + str(self.quantity) + ')'

    # def serial(self):
    #     cart = Cart.objects.all()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_ids = models.CharField(max_length=200, null=True)
    product_ids = models.CharField(max_length=200)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)
    tran_id = models.CharField(max_length=20, null=True)

    delivery_charge = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField()

    confirm = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return str(self.user) + ': ' + str(self.created_at) + '; Confirm: ' + str(self.confirm)

    def save(self, *args, **kwargs):
        carts = Cart.objects.filter(user=self.user)
        carts.delete()
        super(Order, self).save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ': ' + self.comment[0:20]

    def user_avatar(self):
        user = Custom_User.objects.get(user=self.user)
        avatar = user.avatar
        return avatar


class ReplyReview(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rep_comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rep_comment)[0:50]

    def cu(self):
        cu = Custom_User.objects.get(user=self.user)
        return cu


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.IntegerField(default=0)

    def __str__(self):
        return str(self.product) + ': ' + str(self.star) + ' stars'

    def save(self, *args, **kwargs):
        super(Rating, self).save(*args, **kwargs)
        p = Product.objects.get(pk=self.product.id)
        p.star_rating = p.rating()
        p.save()

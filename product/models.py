from django.db    import models
from django.utils import timezone
from user.models  import User

class Menu(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'menus'

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name       = models.CharField(max_length=50)
    price      = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    sale       = models.IntegerField(blank=True)
    category   = models.ForeignKey(Category, on_delete=models.CASCADE)
    like       = models.ManyToManyField(User, through="Wishlist")

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name

class Size(models.Model):
    name    = models.CharField(max_length=100)
    product = models.ManyToManyField(Product, through="ProductSize")

    class Meta:
        db_table = 'sizes'

    def __str__(self):
        return self.name

class ProductSize(models.Model):
    size    = models.ForeignKey(Size, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "product_sizes"

class Image(models.Model):
    image_url = models.URLField(max_length=200)
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "images"

class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table="wishlists"



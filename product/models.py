from django.db    import models
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

class Discount(models.Model):
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "discounts"

class Product(models.Model):
    name        = models.CharField(max_length=50)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes       = models.ManyToManyField(User, through="Wishlist")
    is_in_stock = models.BooleanField(default=True)
    discount    = models.ForeignKey(Discount, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "products"

    def __str__(self):
        return self.name

class Size(models.Model):
    name     = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through="ProductSize")

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



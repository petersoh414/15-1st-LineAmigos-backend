from django.db      import models
from user.models    import User
from product.models import Product


class DeliveryInformation(models.Model):
    basic_address          = models.CharField(max_length=200)
    datail_address         = models.CharField(max_length=200)
    zipcode                = models.IntegerField()
    recipient              = models.CharField(max_length=50)
    recipient_phone_number = models.CharField(max_length=50)

    class Meta:
        db_table = 'delivery_informations'

class Status(models.Model):
    name = models.CharField(max_length =20)

    class Meta:
        db_table = 'status'

class PaymentMethod(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        db_table = 'payment_methods'

class Order(models.Model):
    user                 = models.ForeignKey(User,on_delete=models.CASCADE)
    delivery_information = models.ForeignKey(DeliveryInformation,on_delete=models.CASCADE, null=True)
    status               = models.ForeignKey(Status, on_delete=models.CASCADE)
    order_number         = models.CharField(max_length=30)
    payment_method       = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    delivery_fee         = models.IntegerField(default=3000)

    class Meta:
        db_table = 'orders'

class Cart(models.Model):
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    order    = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'carts'


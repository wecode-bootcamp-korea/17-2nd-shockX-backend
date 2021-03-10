from django.db import models

class User(models.Model):
    email           = models.CharField(max_length=100, unique=True)
    name            = models.CharField(max_length=50)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    seller_level    = models.ForeignKey('SellerLevel', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'users'

class SellerLevel(models.Model):
    name            = models.CharField(max_length=20)
    transaction_fee = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'seller_levels'

class ShippingInformation(models.Model):
    name              = models.CharField(max_length=50)
    country           = models.CharField(max_length=50)
    primary_address   = models.CharField(max_length=200)
    secondary_address = models.CharField(max_length=200, null=True)
    city              = models.CharField(max_length=45)
    state             = models.CharField(max_length=45, null=True)
    postal_code       = models.CharField(max_length=45)
    phone_number      = models.CharField(max_length=45)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)
    user              = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'shipping_informations'

class Portfolio(models.Model):
    user           = models.ForeignKey('User', on_delete=models.CASCADE)
    product_size   = models.ForeignKey('product.ProductSize', on_delete=models.CASCADE)
    purchase_date  = models.DateField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'portfolios'

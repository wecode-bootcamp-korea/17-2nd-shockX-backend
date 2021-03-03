from django.db import models

class Product(models.Model):
    name          = models.CharField(max_length=200)
    model_number  = models.CharField(max_length=100)
    ticker_number = models.CharField(max_length=100)
    color         = models.CharField(max_length=50)
    description   = models.CharField(max_length=2000)
    retail_price  = models.DecimalField(max_digits=10, decimal_places=2)
    release_date  = models.DateTimeField()

    class Meta:
        db_table = 'products'

class Image(models.Model):
    image_url = models.URLField(max_length=2000)
    product   = models.ForeignKey('Product', on_delete=models.CASCADE)

    class Meta:
        db_table = 'images'

class Size(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'sizes'

class ProductSize(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size    = models.ForeignKey('Size', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_sizes'

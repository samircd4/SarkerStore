from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Categorie(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    def __str__(self):
        return self.name

class PriceFilter(models.Model):
    PRICE_FILTER = (
        ('1000 to 10000', '1000 to 10000'),
        ('10000 to 20000', '10000 to 20000'),
        ('20000 to 30000', '20000 to 30000'),
        ('30000 to 40000', '30000 to 40000'),
        ('40000 to 50000', '40000 to 50000'),
    )
    price_filter = models.CharField(choices=PRICE_FILTER, max_length=60)
    
    def __str__(self):
        return self.price_filter


class Product(models.Model):
    STOCK = (
        ('In Stock', 'In Stock'),
        ('Out Of Stock', 'Out Of Stock'),
    )
    
    unique_id = models.CharField(unique=True, max_length=60, null=True, blank=True)
    image = models.ImageField(upload_to='media/product', )
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    info = models.TextField()
    description = models.TextField()
    stock = models.CharField(choices=STOCK, max_length=60)
    status = models.BooleanField(default=True)
    createed_at = models.DateTimeField(auto_now_add=True)
    
    categorie = models.ForeignKey(Categorie, null=True, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, null=True, on_delete=models.CASCADE)
    # color = models.ForeignKey(Color, null=True, on_delete=models.CASCADE)
    price_filter = models.ForeignKey(PriceFilter, null=True, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if self.unique_id is None and self.createed_at and self.id:
            self.unique_id = self.createed_at.strftime('10%Y%m%d30')+str(self.id)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class Images(models.Model):
    img = models.ImageField(upload_to='media/product', )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Veriant(models.Model):
    ram = models.IntegerField()
    rom = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.ram)

class Order(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Packaged', 'Packaged'),
        ('On The Way', 'On The Way'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, blank=True, null=True)
    post_code = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    additional_info = models.TextField(blank=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(choices=STATUS, default='Pending', max_length=50)
    amount = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.FileField(upload_to='media/product')
    quantity = models.IntegerField()
    price = models.IntegerField()
    total = models.IntegerField()
    
    def __str__(self):
        return self.order.user.username
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    p_number = models.CharField(max_length=100)
    p_tra_id = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username

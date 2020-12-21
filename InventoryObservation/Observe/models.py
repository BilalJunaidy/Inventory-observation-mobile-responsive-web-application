from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from .validators import validate_file_extension
from .helpers import file_upload_location

# Create your models here.

class User(AbstractUser):
    pass 

class Enterprise(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return f"{self.id}_{self.name}"


class Client(models.Model):
    clientID = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    enterprise = models.ForeignKey('Enterprise', on_delete=models.CASCADE, related_name = 'clients')

    def __str__(self):
        return f"{self.clientID}_{self.name}"


class Engagement(models.Model):
    engagementID = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    enterprise = models.ForeignKey('Enterprise', on_delete=models.CASCADE, related_name = 'engagements')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name = 'engagements')

    def __str__(self):
        return f"{self.engagementID}_{self.name}"


class StockCount(models.Model):
    name = models.CharField(max_length = 100)
    enterprise = models.ForeignKey('Enterprise', on_delete=models.CASCADE, related_name = 'stockcounts')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name = 'stockcounts')
    engagement = models.ForeignKey('Engagement', on_delete=models.CASCADE, related_name = 'stockcounts')

    def __str__(self):
        return f"{self.name}"


class InventoryList(models.Model):
    UploadedFile = models.FileField(_('Upload Inventory Listing'), upload_to = file_upload_location, validators=[validate_file_extension], max_length = 500)
    RowInvStart = models.IntegerField(_('Row Number for where the Listing starts'), validators=[MinValueValidator(1), MaxValueValidator(1048576)])
    SKUColumn = models.CharField(_('Column which holds the unique SKU/Product code'), max_length=3)
    ProductNameColumn = models.CharField(_('Column which holds the Product Name'), max_length=3, null=True, blank=True)
    ProductCategoryColumn = models.CharField(_('Column which holds the Product category'), max_length=3, null=True, blank=True)
    ProductDescriptionColumn = models.CharField(_('Column which holds the Product description'), max_length=3, null=True, blank=True)
    QuanityColumn = models.CharField(_('Column which holds the Quantity at hand'), max_length=3)
    ValueColumn = models.CharField(_('Column which holds the unit price for the products'), max_length=3, null=True, blank=True)
    enterprise = models.ForeignKey('Enterprise', on_delete=models.CASCADE, related_name = 'inventorylists')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name = 'inventorylists')
    engagement = models.ForeignKey('Engagement', on_delete=models.CASCADE, related_name = 'inventorylists')
    stockcount = models.ForeignKey('StockCount', on_delete=models.CASCADE, related_name = 'inventorylists')

class SKU(models.Model):
    sku = models.CharField(max_length=50)
    product_name = models.CharField(max_length=150)
    product_category = models.CharField(max_length=150)
    product_description = models.CharField(max_length=150)
    quantity_per_client = models.FloatField(validators=[MinValueValidator(0)])
    value = models.FloatField(validators=[MinValueValidator(0)])
    quantity_per_counter = models.FloatField(validators=[MinValueValidator(0)])
    quantity_difference = models.FloatField()
    
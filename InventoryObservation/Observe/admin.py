from django.contrib import admin
from .models import User, Enterprise, Client, Engagement, StockCount, InventoryList, SKU, Image

# Register your models here.
admin.site.register(User)
admin.site.register(Enterprise)
admin.site.register(Client)
admin.site.register(Engagement)
admin.site.register(StockCount)
admin.site.register(InventoryList)
admin.site.register(SKU)
admin.site.register(Image)
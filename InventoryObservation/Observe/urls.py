from django.urls import path

from . import views

urlpatterns = [
    path("upload/", views.upload, name='upload'),
    path("new/", views.new, name='new'),
    path("inventorylist/<str:inventory_list_id>", views.inventorylist, name="inventorylist"),
    path("inventorylist/<str:inventory_list_id>/<str:SKU>", views.SKU, name="SKU"),
]
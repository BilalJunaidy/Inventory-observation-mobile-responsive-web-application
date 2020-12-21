from django.forms import ModelForm
from django import forms 
from .models import User, Enterprise, Client, Engagement, StockCount, InventoryList, SKU 

class InventoryListForm(ModelForm):
    class Meta:
        model = InventoryList
        exclude = ['enterprise', 'client', 'engagement', 'stockcount']
        # fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(InventoryListForm, self).__init__(*args, **kwargs)
    
    # def save(self):
    #     super(InventoryListForm, self).save()

class SKUForm(ModelForm):
    class Meta:
        model = SKU 
        fields = '__all__'
        



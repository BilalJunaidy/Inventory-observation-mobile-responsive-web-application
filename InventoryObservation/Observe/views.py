from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import InventoryListForm, SKUForm, ImageForm
from pathlib import Path
import os 
from django.urls import reverse
from django.conf import settings
from .models import User, Enterprise, Client, Engagement, StockCount, InventoryList, Image
import pandas as pd 
from django.forms import modelformset_factory
from .helpers import ReturnIndex


# Create your views here.

def upload(request):
    
    # The following id's are for now being definied by me, but in the future, these are going to be coming programatically since these id's will be coming from the url.
    enterprise_id = 1
    client_id = 1
    engagement_id = 1
    stockcount_id = 1
    # enterprise_object = Enterprise.objects.get(pk = enterprise_id)
    # client_object = Client.objects.get(pk = client_id)
    # engagement_object = Engagement.objects.get(pk = engagement_id)
    # stockcount_object = StockCount.objects.get(pk = stockcount_id)

    # current_list = InventoryList(enterprise = enterprise_object, client = client_object, engagement = engagement_object, stockcount = stockcount_object)

    if request.method == 'POST':
        # current_list = InventoryList(enterprise_id = 1, client_id = 1, engagement_id = 1, stockcount_id = 1)
        form = InventoryListForm(request.POST, request.FILES)
        # form = InventoryListForm(request.POST, request.FILES, instance = current_list 
        # initial = {
        #     'enterprise_id':enterprise_object,
        #     'client_id':client,
        #     'engagement_id':engagement,
        #     'stockcount_id':stockcount,
        # }
        

        if form.is_valid():    
            # file is saved
            list = form.save(commit = False)
            list.enterprise = Enterprise.objects.get(pk = enterprise_id)
            list.client = Client.objects.get(pk = client_id)
            list.engagement = Engagement.objects.get(pk = engagement_id) 
            list.stockcount = StockCount.objects.get(pk = stockcount_id)   
            list.save() 

            return HttpResponseRedirect(reverse("inventorylist", args=(list.id,)))
            # return HttpResponse(f'You have just made a post request - {list.id}')   
        
        else:
            return render(request, "observe/upload.html", {
            "form": form
        })
    
    else: 
        # myform = InventoryListForm(instance = current_list)
        # for field in myform:
        #     print(field)
        
        # return HttpResponse('you have made a get request')

        return render(request, "observe/upload.html", {
            "form": InventoryListForm()
            # "form": InventoryListForm(instance = current_list)
            })
        #     initial = {
        #     'enterprise_id':enterprise_object,
        #     'client_id':client,
        #     'engagement_id':engagement,
        #     'stockcount_id':stockcount,
        # }
        # return HttpResponse('you have made a get request')

def new(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    return HttpResponse(f'{BASE_DIR}')


def inventorylist(request, inventory_list_id):
    if request.method == 'POST':
        return HttpResponse("you have just made a POST request")
    else:
        Inventory_List_Object = InventoryList.objects.get(pk = inventory_list_id)
        file_ext = Inventory_List_Object.UploadedFile.name.split('.')[-1]
        file_path = os.path.join(settings.MEDIA_ROOT, Inventory_List_Object.UploadedFile.name)

        if file_ext in ['xlsm', 'xlsx']:
            df = pd.read_excel(file_path,engine='openpyxl')
        elif file_ext == 'xls':
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
        
        return render(request, "observe/list.html", {
            "df": df.values.tolist(),
            "inventory_list_id":inventory_list_id,
        })

def SKU(request, inventory_list_id, SKU):


    Inventory_List_Object = InventoryList.objects.get(pk = inventory_list_id)
    file_ext = Inventory_List_Object.UploadedFile.name.split('.')[-1]
    file_path = os.path.join(settings.MEDIA_ROOT, Inventory_List_Object.UploadedFile.name)

    if file_ext in ['xlsm', 'xlsx']:
        df = pd.read_excel(file_path,engine='openpyxl')
    elif file_ext == 'xls':
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)
    
    index = ReturnIndex(df, SKU)[0][0]
    record = df.iloc[index]

    SKU_record = df.iloc[index]['SKU']
    Product_Code_record = df.iloc[index]['Product Code']
    Product_Name_record = df.iloc[index]['Product Name']
    Product_Description_record = df.iloc[index]['Product description']
    Quantity_On_Hand_record = df.iloc[index]['Quantity On Hand']
    Value_record = df.iloc[index]['Value']


    ImageFormSet = modelformset_factory(Image, form = ImageForm, extra = 3)    

    if request.method == 'POST':
        skuform = SKUForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset = Image.objects.none())
        
        
        if skuform.is_valid() and formset.is_valid():
            sku_form = skuform.save(commit = False)
            sku_form.sku = SKU_record
            sku_form.product_name = Product_Name_record
            sku_form.product_category = Product_Code_record
            sku_form.product_description = Product_Description_record
            sku_form.quantity_per_client = Quantity_On_Hand_record
            sku_form.value = Value_record
            sku_form.save()



            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Image(product = sku_form, image = image)
                    photo.save()

            return HttpResponseRedirect(reverse("inventorylist", args=(inventory_list_id,)))

        else:
            return render(request, "observe/SKU.html", {
            "SKUform": skuform,
            "Imageform": formset,
            "inventory_list_id":inventory_list_id,
            "SKU":SKU
        })
    else:

 
        return render(request, "observe/SKU.html", {
            "SKUform": SKUForm(),
            "Imageform": ImageFormSet(queryset = Image.objects.none()),
            "inventory_list_id":inventory_list_id,
            "SKU":SKU,
            "record":record
        })


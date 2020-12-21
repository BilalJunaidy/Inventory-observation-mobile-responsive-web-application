# Generated by Django 3.1.4 on 2020-12-19 12:18

from django.db import migrations, models
import observe.helpers
import observe.validators


class Migration(migrations.Migration):

    dependencies = [
        ('observe', '0005_auto_20201219_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorylist',
            name='UploadedFile',
            field=models.FileField(max_length=500, upload_to=observe.helpers.file_upload_location, validators=[observe.validators.validate_file_extension], verbose_name='Upload Inventory Listing'),
        ),
    ]

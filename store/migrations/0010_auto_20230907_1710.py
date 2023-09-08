# Generated by Django 3.1.6 on 2023-09-07 13:10

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20230907_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='products_order',
            name='avatar_p',
            field=django_resized.forms.ResizedImageField(crop=None, default='', force_format='WEBP', keep_meta=False, quality=75, scale=None, size=[400, 400], upload_to=''),
        ),
        migrations.AddField(
            model_name='products_order',
            name='name_am',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='products_order',
            name='name_en',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='products_order',
            name='name_ru',
            field=models.CharField(default='', max_length=50),
        ),
    ]

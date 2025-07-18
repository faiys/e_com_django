# Generated by Django 5.0.6 on 2025-03-16 14:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productimage', models.ImageField(blank=True, max_length=200, null=True, upload_to='upload/', verbose_name='Product Image')),
                ('productname', models.CharField(max_length=200, verbose_name='Prduct Name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Price')),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('phonenumber', models.CharField(max_length=11, verbose_name='Phone number')),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderno', models.CharField(max_length=200, verbose_name='Order No')),
                ('complete', models.BooleanField(default=False, null=True, verbose_name='Complete')),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('customers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='E_comApp.customers')),
            ],
        ),
        migrations.CreateModel(
            name='shipsaddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=100, verbose_name='Street')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('district', models.CharField(max_length=100, verbose_name='District')),
                ('state', models.CharField(max_length=100, verbose_name='State')),
                ('zipcode', models.CharField(max_length=100, verbose_name='Zip Code')),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('customers', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='E_comApp.customers')),
                ('orders', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='E_comApp.orders')),
            ],
        ),
        migrations.CreateModel(
            name='orderitems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True, verbose_name='Quantity')),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('orders', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='E_comApp.orders')),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='E_comApp.store')),
            ],
        ),
    ]

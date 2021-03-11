# Generated by Django 3.1.6 on 2021-03-11 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('transaction_fee', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'seller_levels',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('seller_level', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='user.sellerlevel')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='ShippingInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('primary_address', models.CharField(max_length=200)),
                ('secondary_address', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=45)),
                ('state', models.CharField(max_length=45, null=True)),
                ('postal_code', models.CharField(max_length=45)),
                ('phone_number', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'shipping_informations',
            },
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateField()),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productsize')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'portfolios',
            },
        ),
    ]

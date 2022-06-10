# Generated by Django 4.0.5 on 2022-06-10 21:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('phone_number', models.CharField(max_length=11, unique=True, verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Почта')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название продукта')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.product', verbose_name='Название продукта')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(verbose_name='Адрес доставки')),
                ('status', models.CharField(choices=[('Создан', 'Создан'), ('Собирается', 'Собирается'), ('Доставляется', 'Доставляется'), ('Доставлен', 'Доставлен'), ('Выдан', 'Выдан'), ('Отменён', 'Отменён')], max_length=12, verbose_name='Статус заказа')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.customer', verbose_name='Закзчик')),
            ],
        ),
    ]

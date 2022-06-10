from django.db import models
from django.core.validators import MinValueValidator


class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone_number = models.CharField(unique=True, max_length=11, verbose_name='Номер телефона')
    email = models.EmailField(unique=True, verbose_name='Почта')

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    STATUSES = (
        ('Создан', 'Создан'),
        ('Собирается', 'Собирается'),
        ('Доставляется', 'Доставляется'),
        ('Доставлен', 'Доставлен'),
        ('Выдан', 'Выдан'),
        ('Отменён', 'Отменён'),
    )
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Закзчик')
    address = models.TextField(verbose_name='Адрес доставки')
    status = models.CharField(choices=STATUSES, max_length=12, verbose_name='Статус заказа')
    created_at = models.DateTimeField()

    def __str__(self):
        return f"#{self.id}: {self.status}"


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название продукта')

    def __str__(self):
        return f"{self.title}"


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Номер заказа')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название продукта')
    quantity = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(1)])
    price = models.FloatField(verbose_name='Цена', validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.product_id} - {self.price}"

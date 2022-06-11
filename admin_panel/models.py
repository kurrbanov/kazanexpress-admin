from django.db import models
from django.core.validators import MinValueValidator


class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    phone_number = models.CharField(unique=True, max_length=11, verbose_name='Номер телефона')
    email = models.EmailField(unique=True, verbose_name='Почта')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Заказчик'
        verbose_name_plural = 'Заказчики'


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
    status = models.CharField(choices=STATUSES, max_length=12, verbose_name='Статус заказа', default='Создан')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return f"#{self.id}: {self.status}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        indexes = [
            models.Index(fields=['status', 'created_at'])
        ]


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название товара')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Номер заказа')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Название товара')
    quantity = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(1)])
    price = models.FloatField(verbose_name='Цена', validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.product_id} - {self.price}"

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

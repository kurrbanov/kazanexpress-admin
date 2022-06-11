from django.contrib import admin

from admin_panel.models import Customer, Order
from admin_panel.filters import OrderStatusFilter, OrderCostFilter, OrderPhoneFilter


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'get_order_page',
        'status',
        'get_customer_name',
        'get_customer_phone_number',
        'get_customer_email',
        'address',
        'get_order_cost',
        'created_at'
    )
    list_filter = (OrderStatusFilter, 'created_at', OrderCostFilter, OrderPhoneFilter)
    readonly_fields = ('status',)

    @admin.display(description='Страница заказа', ordering='id')
    def get_order_page(self, obj: Order):
        return f"Заказ #{obj.id}"

    @admin.display(description='Заказчик')
    def get_customer_name(self, obj: Order):
        return obj.customer_id.name

    @admin.display(description='Телефон заказчика', ordering='customer_id__phone_number')
    def get_customer_phone_number(self, obj: Order):
        return obj.customer_id.phone_number

    @admin.display(description='Почта заказчика')
    def get_customer_email(self, obj: Order):
        return obj.customer_id.email

    @admin.display(description='Стоимость заказа')
    def get_order_cost(self, obj: Order):
        cost = 0
        for order_item in obj.orderitem_set.all():
            cost += (order_item.price * order_item.quantity)
        return cost

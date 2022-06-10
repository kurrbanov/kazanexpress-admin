from django.contrib import admin

from admin_panel.models import Customer, Order, OrderItem


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status',
        'get_customer_name',
        'get_customer_phone_number',
        'get_customer_email',
        'address',
        'created_at')

    @admin.display(description='Заказчик')
    def get_customer_name(self, obj: Order):
        return obj.customer_id.name

    @admin.display(description='Телефон заказчика', ordering='customer_id__phone_number')
    def get_customer_phone_number(self, obj: Order):
        return obj.customer_id.phone_number

    @admin.display(description='Почта заказчика')
    def get_customer_email(self, obj: Order):
        return obj.customer_id.email
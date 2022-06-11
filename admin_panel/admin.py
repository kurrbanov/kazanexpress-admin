from django.contrib import admin
from django.contrib.admin.models import LogEntry, LogEntryManager
from django.contrib.admin.options import get_content_type_for_model
from django.db import models
from django.forms import Textarea
from django.http import HttpResponseRedirect

from admin_panel.models import Customer, Order, OrderItem, Product
from admin_panel.filters import OrderStatusFilter, OrderCostFilter, OrderPhoneFilter, ProductIdFilter, \
    ProductTitleFilter


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.action(description='Отменить выбранные заказы')
def cancel_orders(modeladmin, request, queryset):
    for order in queryset:
        change_message = f"Заказ #{order.id}: {order.status} -> Отменён"
        LogEntry.objects.create(
            user=request.user,
            content_type=get_content_type_for_model(order),
            object_id=order.id,
            action_flag=2,
            change_message=change_message,
            object_repr=order.__str__()
        )
    queryset.update(status='Отменён')


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
    inlines = [OrderItemInline]
    add_form_template = 'admin/order_add_form.html'
    change_form_template = 'admin/order_change_form.html'
    actions = [cancel_orders]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['status']
        return []

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

    def response_change(self, request, obj: Order):
        if "cancel_order" in request.POST:
            prev_status = obj.status
            obj.status = 'Отменён'
            obj.save()
            change_message = f"Заказ #{obj.id}: {prev_status} -> {obj.status}"
            LogEntry.objects.create(
                user=request.user,
                content_type=get_content_type_for_model(obj),
                object_id=obj.id,
                action_flag=2,
                change_message=change_message,
                object_repr=obj.__str__()
            )
            return HttpResponseRedirect('.')
        return super().response_change(request, obj)

    def save_model(self, request, obj: Order, form, change):
        prev_status = obj.status
        super(OrderAdmin, self).save_model(request, obj, form, change)
        if change and prev_status != obj.status:
            change_message = f"Заказ #{obj.id}: {prev_status} -> {obj.status}"
            LogEntry.objects.create(
                user=request.user,
                content_type=get_content_type_for_model(obj),
                object_id=obj.id,
                action_flag=2,
                change_message=change_message,
                object_repr=obj.__str__()
            )

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 2})}
    }

    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = (ProductIdFilter, ProductTitleFilter)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'change_message', 'action_flag')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def get_queryset(self, request):
        queryset = super(LogEntryAdmin, self).get_queryset(request)
        return queryset.filter(action_flag=2).exclude(change_message__exact='[]')

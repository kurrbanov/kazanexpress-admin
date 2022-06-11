from django.contrib import admin
from django.db.models import F, Sum
from django.http.response import HttpResponseBadRequest

from admin_panel.models import Order


class OrderStatusFilter(admin.SimpleListFilter):
    title = 'По статусу заказа'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('Создан', 'Создан'),
            ('Собирается', 'Собирается'),
            ('Доставляется', 'Доставляется'),
            ('Доставлен', 'Доставлен'),
            ('Выдан', 'Выдан'),
            ('Отменён', 'Отменён'),
        ]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(status=self.value())


class OrderInputFilter(admin.SimpleListFilter):
    template = 'admin/order_input_filter.html'

    def lookups(self, request, model_admin):
        return (),

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v) for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class OrderCostFilter(OrderInputFilter):
    title = 'Стоимость в пределах'
    parameter_name = 'cost'

    def queryset(self, request, queryset):
        if self.value() is None or self.value() == '':
            return queryset
        return Order.objects.annotate(mul_result=Sum(F('orderitem__quantity') * F('orderitem__price'))) \
            .filter(mul_result__lte=self.value())

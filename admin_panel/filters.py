from django.contrib import admin
from django.db.models import F, Sum


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
    placeholder = ''

    def lookups(self, request, model_admin):
        return (),

    def choices(self, changelist):
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v) for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        all_choice['placeholder'] = self.placeholder
        yield all_choice


class OrderCostFilter(OrderInputFilter):
    title = 'Стоимость в пределах'
    parameter_name = 'cost'
    placeholder = 'До'

    def queryset(self, request, queryset):
        if self.value() is None or self.value() == '':
            return queryset
        return queryset.annotate(mul_result=Sum(F('orderitem__quantity') * F('orderitem__price'))) \
            .filter(mul_result__lte=self.value())


class OrderPhoneFilter(OrderInputFilter):
    title = 'Номер телефона'
    parameter_name = 'phone_number'
    placeholder = 'Номер телефона'

    def queryset(self, request, queryset):
        if self.value() is None or self.value() == '':
            return queryset
        return queryset.filter(customer_id__phone_number=self.value())


class ProductIdFilter(OrderInputFilter):
    title = 'По ID'
    parameter_name = 'product_id'
    placeholder = 'ID'

    def queryset(self, request, queryset):
        if self.value() is None or self.value() == '':
            return queryset
        return queryset.filter(id=self.value())


class ProductTitleFilter(OrderInputFilter):
    title = 'По наименованию'
    parameter_name = 'product_title'
    placeholder = 'Название'

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(title__icontains=self.value())

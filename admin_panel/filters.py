from django.contrib import admin


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

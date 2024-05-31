# store/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import transaction
from .models.customer import Customer
from .models.orders import Order
from .models.product import Product
from .models.category import Category

class CustomerAdmin(UserAdmin):
    model = Customer
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    actions = ['force_delete_customers']

    @transaction.atomic
    def force_delete_customers(self, request, queryset):
        for customer in queryset:
            self.force_delete_customer(request, customer)
    force_delete_customers.short_description = "Force delete selected customers"

    @transaction.atomic
    def force_delete_customer(self, request, customer):
        # Delete related orders
        Order.objects.filter(customer=customer).delete()
        # Delete related groups and permissions
        customer.groups.clear()
        customer.user_permissions.clear()
        # Finally delete the customer
        customer.delete()

    def delete_model(self, request, obj):
        self.force_delete_customer(request, obj)

    def delete_queryset(self, request, queryset):
        self.force_delete_customers(request, queryset)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'product', 'quantity', 'price', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('customer__email', 'product__name')
    list_editable = ('status',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'description')
    search_fields = ('name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category, CategoryAdmin)

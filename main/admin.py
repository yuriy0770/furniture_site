from django.contrib import admin
from main.models import Category, Furniture


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at', 'product_count']
    list_display_links = ['name']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['created_at']

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = 'Кол-во товаров'


@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'sku', 'price', 'stock',
        'is_active', 'is_featured', 'created_at'
    ]
    list_display_links = ['name']
    list_editable = ['price', 'stock', 'is_active', 'is_featured']
    search_fields = ['name', 'description', 'sku', 'material']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

    # Группировка полей в админке
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'name', 'slug', 'sku', 'description')
        }),
        ('Цены и наличие', {
            'fields': ('price', 'old_price', 'stock', 'is_active', 'is_featured')
        }),
        ('Характеристики', {
            'fields': ('material', 'color', 'dimensions', 'weight',
                       'assembly_required', 'warranty')
        }),
        ('Изображения', {
            'fields': ('image',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

from django.contrib import admin
from .models import Book, User
from django.utils.html import format_html

class BookInventoryInline(admin.TabularInline):
    model = Book
    extra = 1

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'inventory_status', 'created_at')
    list_filter = ('author', 'genre', 'price')
    search_fields = ('title', 'author')
    ordering = ('-created_at',)
    actions = ['mark_as_out_of_stock']

    def inventory_status(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if obj.stock > 0 else 'red',
            'In Stock' if obj.stock > 0 else 'Out of Stock'
        )
    inventory_status.short_description = 'Inventory Status'

    def mark_as_out_of_stock(self, request, queryset):
        rows_updated = queryset.update(stock=0)
        self.message_user(request, f'{rows_updated} books marked as out of stock.')
    mark_as_out_of_stock.short_description = 'Mark selected books as out of stock'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('author')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_active',)
    ordering = ('-date_joined',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('profile')

admin.site.register(Book, BookAdmin)
admin.site.register(User, UserAdmin)

from django.contrib import admin
from .models import (
    Store, Product, ProductImage, Category, Customer, Order, OrderItem,
    Discount, Review, Question, Influencer, EmailCampaign, WhatsAppMessage,
    Theme, StoreTheme, Plugin, StorePlugin, AdCampaign, Wallet, 
    WalletTransaction, Invoice
)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'subdomain', 'owner', 'package', 'status', 'created_at']
    list_filter = ['package', 'status', 'created_at']
    search_fields = ['name', 'subdomain', 'email']
    prepopulated_fields = {'subdomain': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'sku', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_featured', 'store', 'created_at']
    search_fields = ['name', 'sku', 'barcode']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'parent']
    list_filter = ['store']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'store', 'orders_count', 'total_spent']
    list_filter = ['store', 'accepts_marketing', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'store', 'status', 'payment_status', 'total', 'created_at']
    list_filter = ['status', 'payment_status', 'store', 'created_at']
    search_fields = ['order_number', 'customer__email', 'customer__first_name']
    inlines = [OrderItemInline]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['code', 'store', 'type', 'value', 'usage_count', 'is_active', 'valid_until']
    list_filter = ['type', 'is_active', 'store']
    search_fields = ['code']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'rating', 'is_approved', 'is_verified_purchase', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_verified_purchase', 'type']
    search_fields = ['title', 'content', 'customer__email']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'question', 'answered_at', 'is_public']
    list_filter = ['is_public', 'answered_at']
    search_fields = ['question', 'answer']


@admin.register(Influencer)
class InfluencerAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'referral_code', 'commission_rate', 'total_sales', 'is_active']
    list_filter = ['is_active', 'store']
    search_fields = ['name', 'email', 'referral_code']


@admin.register(EmailCampaign)
class EmailCampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'status', 'recipients_count', 'opened_count', 'created_at']
    list_filter = ['status', 'store']
    search_fields = ['name', 'subject']


@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ['type', 'customer', 'store', 'status', 'sent_at', 'created_at']
    list_filter = ['type', 'status', 'store']
    search_fields = ['message', 'customer__email']


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'is_free', 'is_active']
    list_filter = ['is_free', 'is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(StoreTheme)
class StoreThemeAdmin(admin.ModelAdmin):
    list_display = ['store', 'theme', 'is_active', 'installed_at']
    list_filter = ['is_active', 'theme']


@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'is_free', 'is_active']
    list_filter = ['is_free', 'is_active']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(StorePlugin)
class StorePluginAdmin(admin.ModelAdmin):
    list_display = ['store', 'plugin', 'is_active', 'installed_at']
    list_filter = ['is_active', 'plugin']


@admin.register(AdCampaign)
class AdCampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'platform', 'budget', 'spent', 'status', 'start_date']
    list_filter = ['platform', 'status', 'store']
    search_fields = ['name']


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['store', 'balance', 'currency', 'updated_at']
    list_filter = ['currency']
    search_fields = ['store__name']


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'type', 'amount', 'description', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['description']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'store', 'total', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['invoice_number', 'store__name']

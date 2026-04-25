from django.contrib import admin
from .models import (UserProfile, KYCVerification, Equipment, EquipmentListing,
                     Rental, WalletAddress, Transaction, Notification, WithdrawalRequest)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'referral_code', 'created_at']
    search_fields = ['user__username', 'user__email']

@admin.register(KYCVerification)
class KYCAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'status', 'submitted_at']
    list_filter  = ['status']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'daily_rate', 'status', 'featured']
    list_filter  = ['category', 'status']

@admin.register(EquipmentListing)
class EquipmentListingAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'asking_price', 'status', 'created_at']
    list_filter  = ['status', 'category']

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['user', 'equipment', 'start_date', 'end_date', 'total_cost', 'status']

@admin.register(WalletAddress)
class WalletAddressAdmin(admin.ModelAdmin):
    list_display = ['crypto', 'address', 'network', 'is_active']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'amount', 'status', 'created_at']
    list_filter  = ['transaction_type', 'status']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_read', 'created_at']

@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'crypto_type', 'status', 'created_at']

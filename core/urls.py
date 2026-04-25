from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('rentals/', views.my_rentals, name='my_rentals'),
    path('rent/<int:pk>/', views.rent_equipment, name='rent_equipment'),
    path('deposit/', views.deposit_view, name='deposit'),
    path('withdraw/', views.withdraw_view, name='withdraw'),
    path('transactions/', views.transactions_view, name='transactions'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('referral/', views.referral_view, name='referral'),
    # KYC
    path('kyc/', views.kyc_submit, name='kyc_submit'),
    path('kyc/status/', views.kyc_status, name='kyc_status'),
    # Sell / Listings
    path('sell/', views.sell_equipment, name='sell_equipment'),
    path('my-listings/', views.my_listings, name='my_listings'),
    # Receipt
    path('receipt/<int:pk>/', views.view_receipt, name='view_receipt'),
    path('receipt/<int:pk>/download/', views.download_receipt, name='download_receipt'),
    # API
    path('api/popup-check/', views.api_popup_check, name='api_popup_check'),
    path('api/notifications/', views.api_notifications, name='api_notifications'),
    # Admin
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/users/', views.admin_users, name='admin_users'),
    path('admin_dashboard/users/<int:pk>/', views.admin_user_detail, name='admin_user_detail'),
    path('admin_dashboard/add-funds/', views.admin_add_funds, name='admin_add_funds'),
    path('admin_dashboard/rentals/', views.admin_rentals, name='admin_rentals'),
    path('admin_dashboard/wallet-settings/', views.admin_wallet_settings, name='admin_wallet_settings'),
    path('admin_dashboard/transactions/', views.admin_transactions, name='admin_transactions'),
    path('admin_dashboard/transactions/<int:pk>/confirm/', views.admin_confirm_deposit, name='admin_confirm_deposit'),
    path('admin_dashboard/transactions/<int:pk>/reject/', views.admin_reject_deposit, name='admin_reject_deposit'),
    path('admin_dashboard/notifications/', views.admin_notifications, name='admin_notifications'),
    path('admin_dashboard/equipment/', views.admin_equipment, name='admin_equipment'),
    path('admin_dashboard/equipment/add/', views.admin_add_equipment, name='admin_add_equipment'),
    path('admin_dashboard/equipment/<int:pk>/delete/', views.admin_delete_equipment, name='admin_delete_equipment'),
    path('admin_dashboard/kyc/', views.admin_kyc_list, name='admin_kyc_list'),
    path('admin_dashboard/kyc/<int:pk>/approve/', views.admin_kyc_approve, name='admin_kyc_approve'),
    path('admin_dashboard/kyc/<int:pk>/reject/', views.admin_kyc_reject, name='admin_kyc_reject'),
    path('admin_dashboard/kyc/<int:pk>/view/', views.admin_kyc_detail, name='admin_kyc_detail'),
    path('admin_dashboard/listings/', views.admin_listings, name='admin_listings'),
    path('admin_dashboard/listings/<int:pk>/approve/', views.admin_listing_approve, name='admin_listing_approve'),
    path('admin_dashboard/listings/<int:pk>/sold/', views.admin_listing_sold, name='admin_listing_sold'),
    path('admin_dashboard/listings/<int:pk>/reject/', views.admin_listing_reject, name='admin_listing_reject'),
]

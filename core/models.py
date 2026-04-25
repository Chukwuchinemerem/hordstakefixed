from django.db import models
from django.contrib.auth.models import User
import uuid
import random
import string


def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    referral_code = models.CharField(max_length=20, unique=True, default=generate_referral_code)
    referred_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    referral_bonus = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def referral_count(self):
        return UserProfile.objects.filter(referred_by=self).count()

    @property
    def kyc_status(self):
        try:
            return self.user.kyc.status
        except Exception:
            return 'none'


class KYCVerification(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('approved','Approved'),('rejected','Rejected')]
    user          = models.OneToOneField(User, on_delete=models.CASCADE, related_name='kyc')
    full_name     = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    address       = models.TextField()
    ssn           = models.CharField(max_length=20, blank=True)
    id_document   = models.ImageField(upload_to='kyc/ids/')
    selfie        = models.ImageField(upload_to='kyc/selfies/')
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_note    = models.TextField(blank=True)
    submitted_at  = models.DateTimeField(auto_now_add=True)
    reviewed_at   = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"KYC – {self.user.username} ({self.status})"

    class Meta:
        ordering = ['-submitted_at']


class Equipment(models.Model):
    CATEGORY_CHOICES = [
        ('tanker',     'Oil Tanker'),
        ('truck',      'Transport Truck'),
        ('trailer',    'Tanker Trailer'),
        ('storage',    'Storage Tank'),
        ('industrial', 'Industrial Equipment'),
        ('offshore',   'Offshore Equipment'),
        ('pipeline',   'Pipeline Equipment'),
        ('drilling',   'Drilling Equipment'),
    ]
    STATUS_CHOICES = [
        ('available',   'Available'),
        ('rented',      'Rented'),
        ('maintenance', 'Under Maintenance'),
    ]
    name        = models.CharField(max_length=200)
    category    = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    daily_rate  = models.DecimalField(max_digits=12, decimal_places=2)
    image       = models.ImageField(upload_to='equipment/', blank=True, null=True)
    image_url   = models.URLField(max_length=500, blank=True, help_text='External image URL (used if no uploaded image)')
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    capacity    = models.CharField(max_length=100, blank=True)
    location    = models.CharField(max_length=200, blank=True)
    featured    = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def display_image(self):
        """Returns image URL - uploaded file first, then external URL."""
        if self.image:
            return self.image.url
        return self.image_url or ''

    class Meta:
        ordering = ['-featured', 'name']


class EquipmentListing(models.Model):
    """User-submitted equipment for sale on the platform."""
    CATEGORY_CHOICES = Equipment.CATEGORY_CHOICES
    STATUS_CHOICES = [
        ('pending',  'Pending Review'),
        ('approved', 'Approved / For Sale'),
        ('sold',     'Sold'),
        ('rejected', 'Rejected'),
    ]
    PAYMENT_CHOICES = [
        ('bank',   'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
        ('both',   'Bank or Crypto'),
    ]
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title           = models.CharField(max_length=200)
    category        = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description     = models.TextField()
    asking_price    = models.DecimalField(max_digits=15, decimal_places=2)
    year_of_make    = models.CharField(max_length=10, blank=True)
    condition       = models.CharField(max_length=50, blank=True, help_text='e.g. New, Used, Refurbished')
    location        = models.CharField(max_length=200, blank=True)
    image           = models.ImageField(upload_to='listings/', blank=True, null=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method  = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='both')
    # Bank details for receiving payment
    bank_name       = models.CharField(max_length=100, blank=True)
    account_name    = models.CharField(max_length=200, blank=True)
    account_number  = models.CharField(max_length=50, blank=True)
    routing_number  = models.CharField(max_length=20, blank=True)
    # Crypto details for receiving payment
    crypto_wallet   = models.CharField(max_length=200, blank=True)
    crypto_type     = models.CharField(max_length=20, blank=True)
    admin_note      = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} – {self.title} ({self.status})"

    class Meta:
        ordering = ['-created_at']


class Rental(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),('active','Active'),
        ('completed','Completed'),('cancelled','Cancelled'),
    ]
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals')
    equipment     = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    start_date    = models.DateField()
    end_date      = models.DateField()
    duration_days = models.PositiveIntegerField()
    total_cost    = models.DecimalField(max_digits=12, decimal_places=2)
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes         = models.TextField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} – {self.equipment.name}"


class WalletAddress(models.Model):
    CRYPTO_CHOICES = [
        ('USDT','USDT (TRC20)'),('BTC','Bitcoin (BTC)'),
        ('ETH','Ethereum (ETH)'),('SOL','Solana (SOL)'),
    ]
    crypto     = models.CharField(max_length=10, choices=CRYPTO_CHOICES, unique=True)
    address    = models.CharField(max_length=500)
    network    = models.CharField(max_length=100, blank=True)
    is_active  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.crypto} – {self.address[:20]}..."


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('deposit','Deposit'),('withdrawal','Withdrawal'),
        ('rental','Rental Payment'),('referral','Referral Bonus'),
        ('manual','Manual Credit'),
    ]
    STATUS_CHOICES = [
        ('pending','Pending'),('confirmed','Confirmed'),('rejected','Rejected'),
    ]
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount           = models.DecimalField(max_digits=15, decimal_places=2)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    crypto_type      = models.CharField(max_length=10, blank=True)
    tx_hash          = models.CharField(max_length=500, blank=True)
    reference        = models.UUIDField(default=uuid.uuid4, unique=True)
    description      = models.TextField(blank=True)
    rental           = models.ForeignKey(Rental, null=True, blank=True, on_delete=models.SET_NULL)
    receipt_generated = models.BooleanField(default=False)
    popup_shown       = models.BooleanField(default=False)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} – {self.transaction_type} – ${self.amount}"

    class Meta:
        ordering = ['-created_at']


class Notification(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title        = models.CharField(max_length=200)
    message      = models.TextField()
    is_read      = models.BooleanField(default=False)
    is_broadcast = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('approved','Approved'),('rejected','Rejected')]
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals')
    amount         = models.DecimalField(max_digits=15, decimal_places=2)
    crypto_type    = models.CharField(max_length=10)
    wallet_address = models.CharField(max_length=500)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_note     = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} – ${self.amount} ({self.status})"

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Equipment
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('tanker','Oil Tanker'),('truck','Transport Truck'),('trailer','Tanker Trailer'),('storage','Storage Tank'),('industrial','Industrial Equipment'),('offshore','Offshore Equipment'),('pipeline','Pipeline Equipment'),('drilling','Drilling Equipment')], max_length=50)),
                ('description', models.TextField()),
                ('daily_rate', models.DecimalField(decimal_places=2, max_digits=12)),
                ('image', models.ImageField(blank=True, null=True, upload_to='equipment/')),
                ('status', models.CharField(choices=[('available','Available'),('rented','Rented'),('maintenance','Under Maintenance')], default='available', max_length=20)),
                ('capacity', models.CharField(blank=True, max_length=100)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-featured', 'name']},
        ),
        # Rental
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('duration_days', models.PositiveIntegerField()),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=12)),
                ('status', models.CharField(choices=[('pending','Pending'),('active','Active'),('completed','Completed'),('cancelled','Cancelled')], default='pending', max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.equipment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        # WalletAddress
        migrations.CreateModel(
            name='WalletAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crypto', models.CharField(choices=[('USDT','USDT (TRC20)'),('BTC','Bitcoin (BTC)'),('ETH','Ethereum (ETH)'),('SOL','Solana (SOL)')], max_length=10, unique=True)),
                ('address', models.CharField(max_length=500)),
                ('network', models.CharField(blank=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        # Transaction
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('deposit','Deposit'),('withdrawal','Withdrawal'),('rental','Rental Payment'),('referral','Referral Bonus'),('manual','Manual Credit')], max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('status', models.CharField(choices=[('pending','Pending'),('confirmed','Confirmed'),('rejected','Rejected')], default='pending', max_length=20)),
                ('crypto_type', models.CharField(blank=True, max_length=10)),
                ('tx_hash', models.CharField(blank=True, max_length=500)),
                ('reference', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('description', models.TextField(blank=True)),
                ('receipt_generated', models.BooleanField(default=False)),
                ('popup_shown', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
                ('rental', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.rental')),
            ],
            options={'ordering': ['-created_at']},
        ),
        # Notification
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('is_broadcast', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
        # WithdrawalRequest
        migrations.CreateModel(
            name='WithdrawalRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('crypto_type', models.CharField(max_length=10)),
                ('wallet_address', models.CharField(max_length=500)),
                ('status', models.CharField(choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')], default='pending', max_length=20)),
                ('admin_note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        # UserProfile
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('referral_code', models.CharField(default=core.models.generate_referral_code, max_length=20, unique=True)),
                ('referral_bonus', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
                ('referred_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.userprofile')),
            ],
        ),
        # KYCVerification
        migrations.CreateModel(
            name='KYCVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('date_of_birth', models.DateField()),
                ('address', models.TextField()),
                ('ssn', models.CharField(blank=True, max_length=20)),
                ('id_document', models.ImageField(upload_to='kyc/ids/')),
                ('selfie', models.ImageField(upload_to='kyc/selfies/')),
                ('status', models.CharField(choices=[('pending','Pending'),('approved','Approved'),('rejected','Rejected')], default='pending', max_length=20)),
                ('admin_note', models.TextField(blank=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='kyc', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-submitted_at']},
        ),
    ]

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Add image_url to Equipment (this is what's missing in production)
        migrations.AddField(
            model_name='equipment',
            name='image_url',
            field=models.URLField(
                blank=True,
                max_length=500,
                help_text='External image URL (used if no uploaded image)',
                default='',
            ),
            preserve_default=False,
        ),

        # Add EquipmentListing model (new sell feature)
        migrations.CreateModel(
            name='EquipmentListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(
                    choices=[
                        ('tanker','Oil Tanker'),('truck','Transport Truck'),
                        ('trailer','Tanker Trailer'),('storage','Storage Tank'),
                        ('industrial','Industrial Equipment'),('offshore','Offshore Equipment'),
                        ('pipeline','Pipeline Equipment'),('drilling','Drilling Equipment'),
                    ],
                    max_length=50,
                )),
                ('description', models.TextField()),
                ('asking_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('year_of_make', models.CharField(blank=True, max_length=10)),
                ('condition', models.CharField(blank=True, max_length=50)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='listings/')),
                ('status', models.CharField(
                    choices=[
                        ('pending','Pending Review'),('approved','Approved / For Sale'),
                        ('sold','Sold'),('rejected','Rejected'),
                    ],
                    default='pending',
                    max_length=20,
                )),
                ('payment_method', models.CharField(
                    choices=[('bank','Bank Transfer'),('crypto','Cryptocurrency'),('both','Bank or Crypto')],
                    default='both',
                    max_length=10,
                )),
                ('bank_name', models.CharField(blank=True, max_length=100)),
                ('account_name', models.CharField(blank=True, max_length=200)),
                ('account_number', models.CharField(blank=True, max_length=50)),
                ('routing_number', models.CharField(blank=True, max_length=20)),
                ('crypto_wallet', models.CharField(blank=True, max_length=200)),
                ('crypto_type', models.CharField(blank=True, max_length=20)),
                ('admin_note', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='listings',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]

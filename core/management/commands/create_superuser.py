from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection


class Command(BaseCommand):
    help = 'Create default superuser and seed initial data'

    def handle(self, *args, **kwargs):
        # Check if tables exist before trying to use them
        table_names = connection.introspection.table_names()

        if 'auth_user' not in table_names:
            self.stdout.write(self.style.WARNING('Tables not ready yet. Run migrate first.'))
            return

        User = get_user_model()

        # Create superuser
        try:
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='Admin2',
                    email='Admin2@hordstake.com',
                    password='12345678'
                )
                self.stdout.write(self.style.SUCCESS('✅ Superuser created: Admin2 / 12345678'))
            else:
                self.stdout.write('Superuser already exists.')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Superuser step: {e}'))

        # Seed wallet addresses
        try:
            from core.models import WalletAddress
            if 'core_walletaddress' in table_names:
                wallets = [
                    {'crypto': 'USDT', 'address': 'REPLACE_WITH_YOUR_USDT_WALLET_ADDRESS', 'network': 'TRC20'},
                    {'crypto': 'BTC',  'address': 'REPLACE_WITH_YOUR_BTC_WALLET_ADDRESS',  'network': 'Bitcoin Network'},
                    {'crypto': 'ETH',  'address': 'REPLACE_WITH_YOUR_ETH_WALLET_ADDRESS',  'network': 'ERC20'},
                    {'crypto': 'SOL',  'address': 'REPLACE_WITH_YOUR_SOL_WALLET_ADDRESS',  'network': 'Solana Network'},
                ]
                for w in wallets:
                    WalletAddress.objects.get_or_create(
                        crypto=w['crypto'],
                        defaults={'address': w['address'], 'network': w['network']}
                    )
                self.stdout.write(self.style.SUCCESS('✅ Wallet addresses seeded.'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Wallet step: {e}'))

        # Seed equipment
        try:
            from core.models import Equipment
            if 'core_equipment' in table_names and Equipment.objects.count() == 0:
                items = [
                    {
                        'name': 'Crude Oil Tanker — 50,000 BBL',
                        'category': 'tanker',
                        'description': 'Heavy-duty crude oil tanker with 50,000 barrel capacity. Advanced GPS tracking, automated safety systems, and full international maritime certification.',
                        'daily_rate': 4500.00, 'capacity': '50,000 BBL', 'location': 'Houston, TX',
                        'featured': True, 'status': 'available',
                        'image_url': 'https://images.unsplash.com/photo-1519452575417-564c1401ecc0?w=800&q=80',
                    },
                    {
                        'name': 'Industrial Oil Transport Truck',
                        'category': 'truck',
                        'description': '10,000 gallon petroleum transport truck. HazMat certified, GPS monitoring, remote diagnostics, DOT compliance.',
                        'daily_rate': 850.00, 'capacity': '10,000 Gallons', 'location': 'Dallas, TX',
                        'featured': True, 'status': 'available',
                        'image_url': 'https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?w=800&q=80',
                    },
                    {
                        'name': 'Offshore Jack-Up Drilling Rig',
                        'category': 'offshore',
                        'description': 'Self-elevating jack-up drilling platform for shallow water operations up to 300ft depth. Full crew accommodation for 100+ personnel.',
                        'daily_rate': 95000.00, 'capacity': '300 ft depth', 'location': 'Gulf of Mexico',
                        'featured': True, 'status': 'available',
                        'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&q=80',
                    },
                    {
                        'name': 'Underground Safe Storage Tank',
                        'category': 'storage',
                        'description': 'Double-wall fiberglass underground storage tank with cathodic protection, leak detection sensors, and spill containment. Meets EPA and API 650 standards.',
                        'daily_rate': 3200.00, 'capacity': '50,000 Gallons', 'location': 'Oklahoma City, OK',
                        'featured': True, 'status': 'available',
                        'image_url': 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800&q=80',
                    },
                    {
                        'name': 'Oil Tanker Trailer — 8,000 Gal',
                        'category': 'trailer',
                        'description': 'Heavy-duty tanker trailer for petroleum road transport. DOT certified, double-compartment, vacuum-tested, with emergency shut-off valves.',
                        'daily_rate': 1200.00, 'capacity': '8,000 Gallons', 'location': 'Midland, TX',
                        'featured': False, 'status': 'available',
                        'image_url': 'https://images.unsplash.com/photo-1565117100030-4fba1671f83c?w=800&q=80',
                    },
                    {
                        'name': 'LNG Cryogenic Tanker Vessel',
                        'category': 'tanker',
                        'description': 'Specialized liquefied natural gas transport vessel operating at -162°C. Advanced cryogenic insulation, SIGTTO compliant.',
                        'daily_rate': 12000.00, 'capacity': '30,000 m³', 'location': 'Rotterdam, Netherlands',
                        'featured': False, 'status': 'available',
                        'image_url': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80',
                    },
                    {
                        'name': 'Pipeline Inspection Robot — 48"',
                        'category': 'pipeline',
                        'description': 'Advanced inline robotic inspection system with HD cameras, ultrasonic thickness sensors, and real-time wireless data transmission.',
                        'daily_rate': 2200.00, 'capacity': '6–48 inch pipes', 'location': 'Oklahoma City, OK',
                        'featured': False, 'status': 'available',
                        'image_url': 'https://images.unsplash.com/photo-1611270629569-8b357cb88da9?w=800&q=80',
                    },
                    {
                        'name': 'Wellhead Pressure Control System',
                        'category': 'industrial',
                        'description': 'Complete wellhead pressure control system with automated emergency shutdown, SCADA integration, 15,000 PSI rating.',
                        'daily_rate': 3800.00, 'capacity': '15,000 PSI', 'location': 'Midland, TX',
                        'featured': False, 'status': 'available',
                        'image_url': 'https://images.unsplash.com/photo-1574169208507-84376144848b?w=800&q=80',
                    },
                    {
                        'name': 'Onshore Drilling Platform — 2000HP',
                        'category': 'drilling',
                        'description': '2000HP onshore drilling rig with top drive system, automated pipe racking, AC VFD drives, and integrated well monitoring.',
                        'daily_rate': 65000.00, 'capacity': '20,000 ft depth', 'location': 'Permian Basin, TX',
                        'featured': False, 'status': 'available',
                        'image_url': 'https://images.unsplash.com/photo-1543674892-7d64d45df18b?w=800&q=80',
                    },
                    {
                        'name': 'FPSO Vessel (Floating Production)',
                        'category': 'offshore',
                        'description': 'Floating Production, Storage & Offloading vessel with 2 million barrel storage. Fully crewed and operated.',
                        'daily_rate': 250000.00, 'capacity': '2M BBL Storage', 'location': 'North Sea',
                        'featured': False, 'status': 'available',
                        'image_url': 'https://images.unsplash.com/photo-1612965607446-25e1332775ae?w=800&q=80',
                    },
                    {
                        'name': 'Above-Ground Storage Tank Farm',
                        'category': 'storage',
                        'description': 'API 650 above-ground storage tank farm with 5 tanks, bunded containment, vapor recovery systems, and fire protection.',
                        'daily_rate': 8500.00, 'capacity': '500,000 BBL total', 'location': 'Corpus Christi, TX',
                        'featured': False, 'status': 'available',
                        'image_url': 'https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=800&q=80',
                    },
                    {
                        'name': 'Petroleum Vacuum Truck — 5,000 Gal',
                        'category': 'truck',
                        'description': 'Heavy-duty vacuum truck for petroleum by-products, tank cleaning, and spill response.',
                        'daily_rate': 650.00, 'capacity': '5,000 Gallons', 'location': 'Denver, CO',
                        'featured': False, 'status': 'available',
                        'image_url': 'https://images.unsplash.com/photo-1590496793929-36417d3117de?w=800&q=80',
                    },
                ]
                for item in items:
                    Equipment.objects.create(**item)
                self.stdout.write(self.style.SUCCESS(f'✅ Seeded {len(items)} equipment items.'))
            else:
                self.stdout.write('Equipment already exists or table not ready.')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Equipment seeding: {e}'))

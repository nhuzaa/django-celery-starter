from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Role
from devices.models import Device, TestProtocol, TestResult
from django.utils import timezone

class Command(BaseCommand):
    help = "Seed the database with initial data"

    def create_roles(self):
        self.stdout.write("Creating roles...")
        manager_role, _ = Role.objects.get_or_create(
            name='MANAGER',
            defaults={'description': 'Manager role with full access to all devices'}
        )
        engineer_role, _ = Role.objects.get_or_create(
            name='ENGINEER',
            defaults={'description': 'Engineer role with access to assigned devices only'}
        )
        return manager_role, engineer_role

    def create_users(self, manager_role, engineer_role):
        self.stdout.write("Creating users...")
        User = get_user_model()

        # Create or get admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@vitalbio.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': manager_role,
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write("Created admin user")
        else:
            self.stdout.write("Admin user already exists")

        # Create or get manager
        manager, created = User.objects.get_or_create(
            username='manager',
            defaults={
                'email': 'manager@vitalbio.com',
                'first_name': 'John',
                'last_name': 'Manager',
                'role': manager_role,
                'is_staff': True
            }
        )
        if created:
            manager.set_password('manager123')
            manager.save()
            self.stdout.write("Created manager user")
        else:
            self.stdout.write("Manager user already exists")

        # Create or get engineers
        engineers = []
        engineer_data = [
            {'username': 'engineer1', 'email': 'engineer1@vitalbio.com', 'first_name': 'Alice', 'last_name': 'Engineer'},
            {'username': 'engineer2', 'email': 'engineer2@vitalbio.com', 'first_name': 'Bob', 'last_name': 'Engineer'},
            {'username': 'engineer3', 'email': 'engineer3@vitalbio.com', 'first_name': 'Charlie', 'last_name': 'Engineer'},
        ]

        for data in engineer_data:
            engineer, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'role': engineer_role
                }
            )
            if created:
                engineer.set_password('engineer123')
                engineer.save()
                self.stdout.write(f"Created engineer user: {data['username']}")
            else:
                self.stdout.write(f"Engineer user already exists: {data['username']}")
            engineers.append(engineer)

        return admin, manager, engineers

    def create_devices(self, engineers):
        self.stdout.write("Creating devices...")
        devices = []
        device_data = [
            {
                'model_number': 'CM-X1-001',
                'defaults': {
                    'name': 'Cardiac Monitor X1',
                    'device_type': 'MONITORING',
                    'manufacturer': 'VitalBio Medical',
                    'description': 'Advanced cardiac monitoring device with real-time ECG analysis',
                    'assigned_to': engineers[0]
                }
            },
            {
                'model_number': 'NI-N2-002',
                'defaults': {
                    'name': 'Neural Implant N2',
                    'device_type': 'IMPLANT',
                    'manufacturer': 'VitalBio Neuro',
                    'description': 'Next-generation neural interface implant',
                    'assigned_to': engineers[1]
                }
            },
            {
                'model_number': 'BA-B3-003',
                'defaults': {
                    'name': 'Blood Analyzer B3',
                    'device_type': 'DIAGNOSTIC',
                    'manufacturer': 'VitalBio Diagnostics',
                    'description': 'Portable blood analysis system',
                    'assigned_to': engineers[2]
                }
            },
            {
                'model_number': 'TD-T4-004',
                'defaults': {
                    'name': 'Therapy Device T4',
                    'device_type': 'THERAPEUTIC',
                    'manufacturer': 'VitalBio Therapeutics',
                    'description': 'Advanced therapeutic device for rehabilitation',
                    'assigned_to': None
                }
            },
            {
                'model_number': 'CM-X2-005',
                'defaults': {
                    'name': 'Cardiac Monitor X2',
                    'device_type': 'MONITORING',
                    'manufacturer': 'VitalBio Medical',
                    'description': 'Enhanced version of the X1 monitor',
                    'assigned_to': None
                }
            }
        ]

        for data in device_data:
            device, created = Device.objects.get_or_create(
                model_number=data['model_number'],
                defaults=data['defaults']
            )
            if created:
                self.stdout.write(f"Created device: {device.name}")
            else:
                self.stdout.write(f"Device already exists: {device.name}")
            devices.append(device)

        return devices

    def create_test_protocols(self, manager, devices):
        self.stdout.write("Creating test protocols...")
        protocols = []
        protocol_data = [
            {
                'name': 'Basic Functionality Test',
                'version': '1.0',
                'defaults': {
                    'description': 'Standard test for basic device functionality',
                    'status': 'APPROVED',
                    'created_by': manager
                }
            },
            {
                'name': 'Safety Compliance Test',
                'version': '2.1',
                'defaults': {
                    'description': 'Comprehensive safety testing protocol',
                    'status': 'APPROVED',
                    'created_by': manager
                }
            },
            {
                'name': 'Performance Benchmark',
                'version': '1.2',
                'defaults': {
                    'description': 'Performance testing under various conditions',
                    'status': 'REVIEW',
                    'created_by': manager
                }
            }
        ]

        for data in protocol_data:
            protocol, created = TestProtocol.objects.get_or_create(
                name=data['name'],
                version=data['version'],
                defaults=data['defaults']
            )
            if created:
                protocol.devices.set(devices)
                self.stdout.write(f"Created protocol: {protocol.name} v{protocol.version}")
            else:
                self.stdout.write(f"Protocol already exists: {protocol.name} v{protocol.version}")
            protocols.append(protocol)

        return protocols

    def create_test_results(self, engineers, devices, protocols):
        self.stdout.write("Creating test results...")
        test_data = [
            {
                'device': devices[0],
                'protocol': protocols[0],
                'performed_by': engineers[0],
                'defaults': {
                    'status': 'PASS',
                    'notes': 'All basic functions working as expected',
                    'data': {'test_duration': 120, 'error_count': 0}
                }
            },
            {
                'device': devices[1],
                'protocol': protocols[1],
                'performed_by': engineers[1],
                'defaults': {
                    'status': 'FAIL',
                    'notes': 'Safety check failed on power consumption test',
                    'data': {'test_duration': 180, 'error_count': 1}
                }
            },
            {
                'device': devices[2],
                'protocol': protocols[2],
                'performed_by': engineers[2],
                'defaults': {
                    'status': 'IN_PROGRESS',
                    'notes': 'Performance testing in progress',
                    'data': {'test_duration': 60, 'error_count': 0}
                }
            }
        ]

        for data in test_data:
            result, created = TestResult.objects.get_or_create(
                device=data['device'],
                protocol=data['protocol'],
                performed_by=data['performed_by'],
                defaults=data['defaults']
            )
            if created:
                self.stdout.write(f"Created test result for {data['device'].name}")
            else:
                self.stdout.write(f"Test result already exists for {data['device'].name}")

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")
        
        try:
            # Create roles first
            manager_role, engineer_role = self.create_roles()
            
            # Create users and get references
            admin, manager, engineers = self.create_users(manager_role, engineer_role)
            
            # Create devices
            devices = self.create_devices(engineers)
            
            # Create test protocols
            protocols = self.create_test_protocols(manager, devices)
            
            # Create test results
            self.create_test_results(engineers, devices, protocols)
            
            self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
            self.stdout.write("\nLogin credentials:")
            self.stdout.write("Admin: username=admin, password=admin123")
            self.stdout.write("Manager: username=manager, password=manager123")
            self.stdout.write("Engineers: username=engineer1/2/3, password=engineer123")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error during seeding: {str(e)}"))
            raise 
import os
import django
from django.contrib.auth.models import User
from devices.models import Device, TestProtocol, TestResult
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def create_users():
    # Create admin user if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
    
    # Create test engineers
    engineers = []
    for i in range(1, 4):
        username = f'engineer{i}'
        if not User.objects.filter(username=username).exists():
            engineer = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password=f'engineer{i}123',
                first_name=f'Engineer {i}',
                last_name='Test'
            )
            engineers.append(engineer)
    return engineers

def create_devices():
    devices = []
    device_types = ['IMPLANT', 'DIAGNOSTIC', 'MONITORING', 'THERAPEUTIC']
    manufacturers = ['MedTech Inc.', 'HealthCare Systems', 'BioMedical Solutions', 'Advanced Medical Devices']
    
    for i in range(1, 11):
        device = Device.objects.create(
            name=f'Medical Device {i}',
            device_type=device_types[i % len(device_types)],
            model_number=f'MD-{i:03d}',
            manufacturer=manufacturers[i % len(manufacturers)],
            description=f'Advanced medical device for {device_types[i % len(device_types)].lower()} applications'
        )
        devices.append(device)
    return devices

def create_test_protocols(engineers, devices):
    protocols = []
    statuses = ['DRAFT', 'REVIEW', 'APPROVED', 'ARCHIVED']
    
    for i in range(1, 11):
        protocol = TestProtocol.objects.create(
            name=f'Test Protocol {i}',
            version=f'1.{i}',
            description=f'Comprehensive testing protocol for medical devices',
            status=statuses[i % len(statuses)],
            created_by=engineers[i % len(engineers)]
        )
        # Assign random devices to each protocol
        protocol.devices.set(devices[i % 3:i % 3 + 3])
        protocols.append(protocol)
    return protocols

def create_test_results(devices, protocols, engineers):
    results = []
    statuses = ['PASS', 'FAIL', 'IN_PROGRESS', 'INVALID']
    
    for i in range(1, 11):
        result = TestResult.objects.create(
            device=devices[i % len(devices)],
            protocol=protocols[i % len(protocols)],
            performed_by=engineers[i % len(engineers)],
            status=statuses[i % len(statuses)],
            start_time=timezone.now(),
            end_time=timezone.now() if statuses[i % len(statuses)] != 'IN_PROGRESS' else None,
            notes=f'Test result notes for device {devices[i % len(devices)].name}',
            data={
                'test_id': f'TEST-{i:03d}',
                'parameters': {
                    'temperature': 25.5,
                    'humidity': 45,
                    'pressure': 101.3
                },
                'measurements': [1.2, 2.3, 3.4, 4.5]
            }
        )
        results.append(result)
    return results

def seed_database():
    print("Starting database seeding...")
    
    # Create users
    print("Creating users...")
    engineers = create_users()
    
    # Create devices
    print("Creating devices...")
    devices = create_devices()
    
    # Create test protocols
    print("Creating test protocols...")
    protocols = create_test_protocols(engineers, devices)
    
    # Create test results
    print("Creating test results...")
    results = create_test_results(devices, protocols, engineers)
    
    print("Database seeding completed successfully!")
    print(f"Created: {len(engineers)} engineers, {len(devices)} devices, {len(protocols)} protocols, {len(results)} test results")

if __name__ == '__main__':
    seed_database() 
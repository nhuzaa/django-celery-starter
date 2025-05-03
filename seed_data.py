from django.contrib.auth import get_user_model
from users.models import Role
from devices.models import Device, TestProtocol, TestResult
from django.utils import timezone
import json

def create_roles():
    print("Creating roles...")
    Role.objects.get_or_create(name='MANAGER', defaults={'description': 'Manager role with full access to all devices'})
    Role.objects.get_or_create(name='ENGINEER', defaults={'description': 'Engineer role with access to assigned devices only'})

def create_users():
    print("Creating users...")
    User = get_user_model()
    manager_role = Role.objects.get(name='MANAGER')
    engineer_role = Role.objects.get(name='ENGINEER')

    # Create admin user
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@vitalbio.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        role=manager_role
    )

    # Create manager
    manager = User.objects.create_user(
        username='manager',
        email='manager@vitalbio.com',
        password='manager123',
        first_name='John',
        last_name='Manager',
        role=manager_role
    )

    # Create engineers
    engineers = []
    engineer_data = [
        {'username': 'engineer1', 'email': 'engineer1@vitalbio.com', 'first_name': 'Alice', 'last_name': 'Engineer'},
        {'username': 'engineer2', 'email': 'engineer2@vitalbio.com', 'first_name': 'Bob', 'last_name': 'Engineer'},
        {'username': 'engineer3', 'email': 'engineer3@vitalbio.com', 'first_name': 'Charlie', 'last_name': 'Engineer'},
    ]

    for data in engineer_data:
        engineer = User.objects.create_user(
            **data,
            password='engineer123',
            role=engineer_role
        )
        engineers.append(engineer)

    return admin, manager, engineers

def create_devices(engineers):
    print("Creating devices...")
    devices = []
    device_data = [
        {
            'name': 'Cardiac Monitor X1',
            'device_type': 'MONITORING',
            'model_number': 'CM-X1-001',
            'manufacturer': 'VitalBio Medical',
            'description': 'Advanced cardiac monitoring device with real-time ECG analysis',
            'assigned_to': engineers[0]
        },
        {
            'name': 'Neural Implant N2',
            'device_type': 'IMPLANT',
            'model_number': 'NI-N2-002',
            'manufacturer': 'VitalBio Neuro',
            'description': 'Next-generation neural interface implant',
            'assigned_to': engineers[1]
        },
        {
            'name': 'Blood Analyzer B3',
            'device_type': 'DIAGNOSTIC',
            'model_number': 'BA-B3-003',
            'manufacturer': 'VitalBio Diagnostics',
            'description': 'Portable blood analysis system',
            'assigned_to': engineers[2]
        },
        {
            'name': 'Therapy Device T4',
            'device_type': 'THERAPEUTIC',
            'model_number': 'TD-T4-004',
            'manufacturer': 'VitalBio Therapeutics',
            'description': 'Advanced therapeutic device for rehabilitation',
            'assigned_to': None
        },
        {
            'name': 'Cardiac Monitor X2',
            'device_type': 'MONITORING',
            'model_number': 'CM-X2-005',
            'manufacturer': 'VitalBio Medical',
            'description': 'Enhanced version of the X1 monitor',
            'assigned_to': None
        }
    ]

    for data in device_data:
        device = Device.objects.create(**data)
        devices.append(device)

    return devices

def create_test_protocols(manager, devices):
    print("Creating test protocols...")
    protocols = []
    protocol_data = [
        {
            'name': 'Basic Functionality Test',
            'version': '1.0',
            'description': 'Standard test for basic device functionality',
            'status': 'APPROVED',
            'created_by': manager
        },
        {
            'name': 'Safety Compliance Test',
            'version': '2.1',
            'description': 'Comprehensive safety testing protocol',
            'status': 'APPROVED',
            'created_by': manager
        },
        {
            'name': 'Performance Benchmark',
            'version': '1.2',
            'description': 'Performance testing under various conditions',
            'status': 'REVIEW',
            'created_by': manager
        }
    ]

    for data in protocol_data:
        protocol = TestProtocol.objects.create(**data)
        protocol.devices.set(devices)  # Associate with all devices
        protocols.append(protocol)

    return protocols

def create_test_results(engineers, devices, protocols):
    print("Creating test results...")
    test_data = [
        {
            'device': devices[0],
            'protocol': protocols[0],
            'performed_by': engineers[0],
            'status': 'PASS',
            'notes': 'All basic functions working as expected',
            'data': {'test_duration': 120, 'error_count': 0}
        },
        {
            'device': devices[1],
            'protocol': protocols[1],
            'performed_by': engineers[1],
            'status': 'FAIL',
            'notes': 'Safety check failed on power consumption test',
            'data': {'test_duration': 180, 'error_count': 1}
        },
        {
            'device': devices[2],
            'protocol': protocols[2],
            'performed_by': engineers[2],
            'status': 'IN_PROGRESS',
            'notes': 'Performance testing in progress',
            'data': {'test_duration': 60, 'error_count': 0}
        }
    ]

    for data in test_data:
        TestResult.objects.create(**data)

def main():
    print("Starting database seeding...")
    
    # Create roles first
    create_roles()
    
    # Create users and get references
    admin, manager, engineers = create_users()
    
    # Create devices
    devices = create_devices(engineers)
    
    # Create test protocols
    protocols = create_test_protocols(manager, devices)
    
    # Create test results
    create_test_results(engineers, devices, protocols)
    
    print("Database seeding completed successfully!")
    print("\nLogin credentials:")
    print("Admin: username=admin, password=admin123")
    print("Manager: username=manager, password=manager123")
    print("Engineers: username=engineer1/2/3, password=engineer123")

if __name__ == '__main__':
    main() 
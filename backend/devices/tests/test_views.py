from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser, Role
from devices.models import Device, TestProtocol, TestResult

class DeviceViewSetTests(TestCase):
    def setUp(self):
        # Create roles
        self.engineer_role = Role.objects.create(name='ENGINEER')
        self.admin_role = Role.objects.create(name='MANAGER')
        
        # Create test users
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.admin_user.role = self.admin_role
        self.admin_user.save()
        
        self.engineer = CustomUser.objects.create_user(
            username='engineer',
            email='engineer@test.com',
            password='engineer123'
        )
        self.engineer.role = self.engineer_role
        self.engineer.save()
        
        # Create test device
        self.device = Device.objects.create(
            name='Test Device',
            device_type='DIAGNOSTIC',
            model_number='TEST-001',
            manufacturer='Test Corp',
            description='Test device description',
            assigned_to=self.engineer
        )
        
        # Setup API client
        self.client = APIClient()
        
    def test_list_devices_admin(self):
        """Test that admin can list all devices"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('devicelist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_devices_engineer(self):
        """Test that engineer can only see assigned devices"""
        self.client.force_authenticate(user=self.engineer)
        url = reverse('devicelist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Device')

class TestProtocolViewSetTests(TestCase):
    def setUp(self):
        # Create roles
        self.admin_role = Role.objects.create(name='MANAGER')
        
        # Create admin user
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.admin_user.role = self.admin_role
        self.admin_user.save()
        
        # Create test device
        self.device = Device.objects.create(
            name='Test Device',
            device_type='DIAGNOSTIC',
            model_number='TEST-001',
            manufacturer='Test Corp',
            description='Test device description'
        )
        
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        
    def test_create_protocol(self):
        """Test creating a new test protocol"""
        url = reverse('protocols-list')
        data = {
            'name': 'New Protocol',
            'version': '1.0',
            'status': 'DRAFT',
            'description': 'Test protocol',
            'devices': [self.device.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestProtocol.objects.count(), 1)
        self.assertEqual(TestProtocol.objects.get().name, 'New Protocol')

class TestResultViewSetTests(TestCase):
    def setUp(self):
        # Create roles
        self.admin_role = Role.objects.create(name='MANAGER')
        self.engineer_role = Role.objects.create(name='ENGINEER')
        
        # Create users
        self.admin_user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.admin_user.role = self.admin_role
        self.admin_user.save()
        
        self.engineer = CustomUser.objects.create_user(
            username='engineer',
            email='engineer@test.com',
            password='engineer123'
        )
        self.engineer.role = self.engineer_role
        self.engineer.save()
        
        # Create test device and protocol
        self.device = Device.objects.create(
            name='Test Device',
            device_type='DIAGNOSTIC',
            model_number='TEST-001',
            manufacturer='Test Corp',
            description='Test device description',
            assigned_to=self.engineer
        )
        self.protocol = TestProtocol.objects.create(
            name='Test Protocol',
            version='1.0',
            status='APPROVED',
            description='Test protocol description',
            created_by=self.admin_user
        )
        self.protocol.devices.add(self.device)
        
        self.client = APIClient()
        
    def test_create_result(self):
        """Test creating a new test result"""
        self.client.force_authenticate(user=self.engineer)
        url = reverse('results-list')
        data = {
            'device': self.device.id,
            'protocol': self.protocol.id,
            'status': 'IN_PROGRESS',
            'start_time': '2024-03-20T10:00:00Z'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestResult.objects.count(), 1)

    def test_complete_result(self):
        """Test completing a test result"""
        # Create a test result first
        result = TestResult.objects.create(
            device=self.device,
            protocol=self.protocol,
            status='IN_PROGRESS',
            performed_by=self.engineer,
            start_time='2024-03-20T10:00:00Z'
        )
        
        self.client.force_authenticate(user=self.engineer)
        url = reverse('results-complete', args=[result.id])
        data = {
            'status': 'PASS',
            'end_time': '2024-03-20T11:00:00Z',
            'notes': 'Test completed successfully'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result.refresh_from_db()
        self.assertEqual(result.status, 'PASS') 
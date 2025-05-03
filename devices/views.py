from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Device, TestProtocol, TestResult
from .serializers import DeviceSerializer, TestProtocolSerializer, TestResultSerializer
from users.permissions import DeviceAccessPermission

class DeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing medical devices.
    
    This endpoint allows you to:
    - List all devices
    - Create new devices
    - Retrieve device details
    - Update devices
    - Delete devices
    - Assign devices to engineers
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated, DeviceAccessPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['device_type', 'manufacturer', 'assigned_to']
    search_fields = ['name', 'model_number', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']

    def get_queryset(self):
        """
        Filter devices based on user role:
        - Managers see all devices
        - Engineers see only their assigned devices
        """
        if self.request.user.is_manager():
            return Device.objects.all()
        elif self.request.user.is_engineer():
            return Device.objects.filter(assigned_to=self.request.user)
        return Device.objects.none()

    @swagger_auto_schema(
        operation_description="Assign a device to an engineer",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the user to assign the device to'),
            },
            required=['user_id']
        ),
        responses={200: "Device assigned successfully", 400: "Invalid request"}
    )
    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        device = self.get_object()
        user_id = request.data.get('user_id')
        if user_id:
            device.assigned_to_id = user_id
            device.save()
            return Response({'status': 'device assigned'})
        return Response({'status': 'user_id required'}, status=400)

class TestProtocolViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing test protocols.
    
    This endpoint allows you to:
    - List all protocols
    - Create new protocols
    - Retrieve protocol details
    - Update protocols
    - Delete protocols
    """
    queryset = TestProtocol.objects.all()
    serializer_class = TestProtocolSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'created_by']
    search_fields = ['name', 'version', 'description']
    ordering_fields = ['name', 'created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TestResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing test results.
    
    This endpoint allows you to:
    - List all test results
    - Create new test results
    - Retrieve test result details
    - Update test results
    - Delete test results
    - Complete tests
    """
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'device', 'protocol', 'performed_by']
    search_fields = ['notes', 'device__name', 'protocol__name']
    ordering_fields = ['start_time', 'end_time', 'created_at']

    @swagger_auto_schema(
        operation_description="Complete a test and record its results",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['PASS', 'FAIL', 'INVALID'], description='Final status of the test'),
                'end_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='When the test was completed'),
                'notes': openapi.Schema(type=openapi.TYPE_STRING, description='Additional notes about the test'),
            },
            required=['status']
        ),
        responses={200: "Test completed successfully", 400: "Test already completed or invalid request"}
    )
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        test_result = self.get_object()
        if test_result.status == 'IN_PROGRESS':
            test_result.status = request.data.get('status', 'PASS')
            test_result.end_time = request.data.get('end_time')
            test_result.notes = request.data.get('notes', '')
            test_result.save()
            return Response({'status': 'test completed'})
        return Response({'status': 'test already completed'}, status=400) 
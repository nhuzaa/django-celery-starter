from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Device, TestProtocol, TestResult

CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class DeviceSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )
    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ['id', 'name', 'device_type', 'model_number', 'manufacturer', 
                 'description', 'assigned_to', 'assigned_to_name', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_assigned_to_name(self, obj):
        return obj.assigned_to.get_full_name() if obj.assigned_to else None

class TestProtocolSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False
    )
    created_by_name = serializers.SerializerMethodField()
    devices = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all(),
        many=True
    )

    class Meta:
        model = TestProtocol
        fields = ['id', 'name', 'version', 'description', 'status', 
                 'created_by', 'created_by_name', 'devices', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_created_by_name(self, obj):
        return obj.created_by.get_full_name() if obj.created_by else None

class TestResultSerializer(serializers.ModelSerializer):
    performed_by = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False
    )
    performed_by_name = serializers.SerializerMethodField()
    device_name = serializers.SerializerMethodField()
    protocol_name = serializers.SerializerMethodField()

    class Meta:
        model = TestResult
        fields = ['id', 'device', 'device_name', 'protocol', 'protocol_name',
                 'performed_by', 'performed_by_name', 'status', 'start_time',
                 'end_time', 'notes', 'data', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_performed_by_name(self, obj):
        return obj.performed_by.get_full_name() if obj.performed_by else None

    def get_device_name(self, obj):
        return obj.device.name if obj.device else None

    def get_protocol_name(self, obj):
        return obj.protocol.name if obj.protocol else None

    def create(self, validated_data):
        validated_data['performed_by'] = self.context['request'].user
        return super().create(validated_data) 
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Device, TestProtocol, TestResult

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class DeviceSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='assigned_to',
        write_only=True,
        required=False
    )

    class Meta:
        model = Device
        fields = '__all__'

class TestProtocolSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    devices = DeviceSerializer(many=True, read_only=True)
    device_ids = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all(),
        source='devices',
        many=True,
        write_only=True
    )

    class Meta:
        model = TestProtocol
        fields = '__all__'

class TestResultSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)
    protocol = TestProtocolSerializer(read_only=True)
    performed_by = UserSerializer(read_only=True)
    device_id = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all(),
        source='device',
        write_only=True
    )
    protocol_id = serializers.PrimaryKeyRelatedField(
        queryset=TestProtocol.objects.all(),
        source='protocol',
        write_only=True
    )

    class Meta:
        model = TestResult
        fields = '__all__'
        read_only_fields = ('performed_by', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['performed_by'] = self.context['request'].user
        return super().create(validated_data) 
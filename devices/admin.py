from django.contrib import admin
from .models import Device, TestProtocol, TestResult

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_type', 'model_number', 'manufacturer', 'assigned_to', 'created_at')
    list_filter = ('device_type', 'manufacturer', 'assigned_to', 'created_at')
    search_fields = ('name', 'model_number', 'manufacturer', 'description')
    raw_id_fields = ('assigned_to',)
    date_hierarchy = 'created_at'

@admin.register(TestProtocol)
class TestProtocolAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_by', 'created_at')
    search_fields = ('name', 'version', 'description')
    filter_horizontal = ('devices',)
    raw_id_fields = ('created_by',)
    date_hierarchy = 'created_at'

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('device', 'protocol', 'performed_by', 'status', 'start_time', 'end_time')
    list_filter = ('status', 'performed_by', 'start_time', 'end_time')
    search_fields = ('device__name', 'protocol__name', 'notes')
    raw_id_fields = ('device', 'protocol', 'performed_by')
    date_hierarchy = 'created_at' 
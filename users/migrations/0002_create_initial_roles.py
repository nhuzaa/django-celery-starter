from django.db import migrations

def create_initial_roles(apps, schema_editor):
    Role = apps.get_model('users', 'Role')
    Role.objects.create(name='MANAGER', description='Manager role with full access to all devices')
    Role.objects.create(name='ENGINEER', description='Engineer role with access to assigned devices only')

def reverse_roles(apps, schema_editor):
    Role = apps.get_model('users', 'Role')
    Role.objects.filter(name__in=['MANAGER', 'ENGINEER']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_roles, reverse_roles),
    ] 
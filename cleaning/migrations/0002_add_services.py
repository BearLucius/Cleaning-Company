
from django.db import migrations

def add_services(apps, schema_editor):
    Service = apps.get_model('cleaning', 'Service')
    services = [
        ('general_cleaning', 'Общий клининг'),
        ('deep_cleaning', 'Генеральная уборка'),
        ('post_construction_cleaning', 'Послестроительная уборка'),
        ('dry_cleaning', 'Химчистка'),
    ]
    for service_name, service_display in services:
        Service.objects.create(name=service_name)

class Migration(migrations.Migration):

    dependencies = [
        ('cleaning', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_services),
    ]

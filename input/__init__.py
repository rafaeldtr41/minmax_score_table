import os
import django





#Configuring Django ORM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'min_max_database_config.settings')
django.setup()
print(django.get_version())
#!/bin/bash

# Wait for PostgreSQL to be ready It should be ready
echo "Waiting for PostgreSQL to be ready..."

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
"

echo "Super User Created :D"

# Run seed data script
echo "Running seed data script..."
python manage.py seed 
echo "Database initialization complete!" 
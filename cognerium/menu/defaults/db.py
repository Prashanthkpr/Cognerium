from django.apps import apps


def create_super_user(apps, schema_editor):
    User = apps.get_model('users', 'User')
    if not User.objects.filter(email="prashanthk432@gmail.com").exists():
        User.objects.create_superuser(
            username='prashanthkpr', email='prashanthk432@gmail.com',
            password='prashanthkpr', first_name="Prashanth",
            last_name="Kasam", is_staff=True, is_active=True
        )

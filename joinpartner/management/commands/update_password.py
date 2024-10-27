from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Update password for users with defaultpassword'

    def handle(self, *args, **kwargs):
        users = User.objects.filter(password='defaultpassword')
        for user in users:
            user.set_password('defaultpassword')
            user.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated passwords'))

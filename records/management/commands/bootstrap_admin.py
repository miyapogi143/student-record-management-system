import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a one-time administrator from bootstrap environment variables."

    def handle(self, *args, **options):
        username = os.environ.get("BOOTSTRAP_ADMIN_USERNAME")
        password = os.environ.get("BOOTSTRAP_ADMIN_PASSWORD")
        if not username or not password:
            self.stdout.write("No administrator bootstrap credentials configured.")
            return

        user_model = get_user_model()
        if user_model.objects.filter(username=username).exists():
            raise CommandError("The requested bootstrap username already exists.")

        user_model.objects.create_superuser(username=username, password=password)
        self.stdout.write(self.style.SUCCESS("Administrator account created."))

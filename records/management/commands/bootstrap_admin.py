import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the initial administrator from temporary deployment settings."

    def handle(self, *args, **options):
        username = os.environ.get("BOOTSTRAP_ADMIN_USERNAME")
        password = os.environ.get("BOOTSTRAP_ADMIN_PASSWORD")
        if not username or not password:
            self.stdout.write("No administrator bootstrap credentials configured.")
            return

        user_model = get_user_model()
        if user_model.objects.filter(username=username).exists():
            self.stdout.write("Bootstrap administrator already exists.")
            return

        user_model.objects.create_superuser(username=username, password=password)
        self.stdout.write(self.style.SUCCESS("Administrator account created."))

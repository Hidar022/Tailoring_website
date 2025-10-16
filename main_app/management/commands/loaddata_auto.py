from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Automatically loads data.json after migrations"

    def handle(self, *args, **kwargs):
        try:
            call_command("loaddata", "data.json")
            self.stdout.write(self.style.SUCCESS("✅ Data loaded successfully."))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"⚠️ Could not load data: {e}"))

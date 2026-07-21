from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from cinemas.models import Showtime

class Command(BaseCommand):
    help = "Delete old showtimes"

    def handle(self, *args, **kwargs):
        cutoff = timezone.now() - timedelta(days=2)
        print(Showtime.objects.all())
        deleted, _ = Showtime.objects.filter(
            start_time__lt=cutoff
        ).delete()

        self.stdout.write(f"Deleted {deleted} old showtimes")
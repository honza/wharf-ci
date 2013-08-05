from django.core.management.base import BaseCommand, CommandError
from web.models import Build
from web.tasks import _run_build


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            b = Build.objects.get(pk=args[0])
        except Build.DoesNotExist:
            raise CommandError('Build not found')

        _run_build(b)

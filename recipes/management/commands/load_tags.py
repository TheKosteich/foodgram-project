from django.core.management.base import BaseCommand

from taggit.models import Tag


class Command(BaseCommand):
    help = 'Create base tags to database'

    def handle(self, *args, **options):
        Tag.objects.get_or_create(name='breakfast')
        Tag.objects.get_or_create(name='lunch')
        Tag.objects.get_or_create(name='dinner')
        print('Tags initialized successfully')

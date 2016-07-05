import os
from django.conf import settings
from django.core.management import BaseCommand
from archapp.populatedb import populate_from_excel


class Command(BaseCommand):
    help = "Fills database from excel file"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('filename', nargs = '+', type = str) 

    def handle(self, *args, **options):
        if options['filename']:
            populate_from_excel(options['filename'][0])
        else:
            self.stdout.write('Please provide a filename to import from')

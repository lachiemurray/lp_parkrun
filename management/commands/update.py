from django.core.management.base import BaseCommand, CommandError 
from lp_parkrun.models import User, Event

class Command(BaseCommand): 
    args = '< >' 
    help = 'Update local parkrun database'

    def handle(self, *args, **options): 
    
        self.stdout.write('Local parkrun database updated.\n')
from django.conf import settings
from frontcast import local_settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<csv absolute path>'
    help = 'Import a list of user from a csv file along with their Affiliation. Csv file must be comma separated, and affiliation name must be inside WALT_AFFILIATIONS local settings'


    def handle(self, *args, **options):
        self.stdout.write( "args" )
        print local_settings.WALT_AFFILIATIONS

        #if not os.path.exists( options.csv ):
        #error( message="csv file was not found.", parser=parser )

        # f = open( options.csv, 'rb' )
        # c = csv.DictReader( f, delimiter=options.delimiter )

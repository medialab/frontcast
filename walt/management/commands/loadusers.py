from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = '<csv absolute path>'
    help = 'Import a list of user from a csv file along with their Affiliation. Csv file must be comma separated, and affiliation name must be a group name'


    def handle(self, *args, **options):
        self.stdout.write( "args" )

        #if not os.path.exists( options.csv ):
        #error( message="csv file was not found.", parser=parser )

        # f = open( options.csv, 'rb' )
        # c = csv.DictReader( f, delimiter=options.delimiter )

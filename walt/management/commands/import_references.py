import os, csv, codecs

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from walt.models import Document
from walt.utils import unicode_dict_reader

class Command(BaseCommand):
    args = '<csv absolute path>'
    help = 'Import a list of user from a csv file along with their Affiliation. Csv file must be comma separated, and affiliation name must be a group name'
    option_list = BaseCommand.option_list + (
        make_option('--csv',
            action='store',
            dest='csv',
            default=False,
            help='csv file of references'),
        make_option('--owner',
            action='store',
            dest='owner',
            default=False,
            help='owner username'),
    )

    def handle(self, *args, **options):
        # set default owner if ldap is not
        self.stdout.write("\n------------------------------------------\n\n    welcome to import_reference script\n    ==================================\n\n\n\n")
            
        if not os.path.exists( options['csv']):
            self.stdout.write("file loaded correctly")
            return

        f = open(options['csv'], 'rb')
        c = unicode_dict_reader(f)

        # owner will be used as default owner; you can change it later
        owner = User.objects.get(username=options['owner'])
        self.stdout.write("    using %s as owner" % owner.username)

        for counter,row in enumerate(c):
            self.stdout.write("    (line %s)" % counter)
            user_fullname = row['user_fullname']
            

            # cfr Document Model
            document_title = row['document_title']
            document_reference = row['document_reference']

            # check for already exhisting stuffs
            documents = Document.objects.filter(reference=document_reference)
            if documents.count() == 0:
                # create object
                self.stdout.write("        creating Document object")
                self.stdout.write("        - refid : %s" % document_reference)
                self.stdout.write("        - title : %s" % document_title)
                d = Document(
                    title=document_title,
                    reference=document_reference,
                    language='en',
                    owner=owner
                )

                d.save()

                self.stdout.write("        - id    :  %s (created)" % d.id)
                self.stdout.write("        - slug  :  %s" % d.slug)
            else:
                d = documents[0]
                self.stdout.write("        Document reference %s already stored" % document_reference)
                self.stdout.write("        - refid : %s" % d.reference)
                self.stdout.write("        - id    : %s" % d.id)
                self.stdout.write("        - title : %s" % d.title)
                self.stdout.write("        - slug  : %s" % d.slug)

                
            

            
            self.stdout.write("\n")
    
        



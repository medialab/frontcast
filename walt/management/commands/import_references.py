import os, csv
from optparse import make_option

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from walt.models import Document, Tag
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
        
        self.stdout.write("    loading file %s" % options['csv'])
        if not os.path.exists( options['csv']):
            self.stdout.write("    file %s not found" % options['csv'])
            return

        f = open(options['csv'], 'rb')
        c = unicode_dict_reader(f)

        # owner will be used as default owner; you can change it later
        owner = User.objects.get(username=options['owner'])
        self.stdout.write("    using <user:%s> as owner\n\n" % owner.username)
        document_translate_types = {
          'video': 'ControversyVideo'
        }

        raw_input("press any key to continue");

        for counter,row in enumerate(c):
            self.stdout.write("    (line %s)" % counter)
            
            # author
            first_name = row['first_name'].strip()
            last_name = row['last_name'].strip()
            affiliation = row['affiliation'].strip()
            tag_author = "%s, %s (%s)" % (last_name, first_name, affiliation)

            # cfr Document Model
            document_title = row['document_title']
            document_reference = row['document_reference']
            document_type = document_translate_types[row['task'].strip()]

            tag_year = row['document_tag_year']
            tag_course = row['course_code']
            

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
                    type=document_type,
                    language='en',
                    owner=owner
                )
                d.save()

                self.stdout.write("        - id    :  %s (created)" % d.id)
                self.stdout.write("        - slug  :  %s" % d.slug)
            else:
                d = documents[0]
                self.stdout.write("        Document reference %s already stored" % document_reference)
                if d.type != document_type:
                  while True:
                    allow_changes = raw_input("        ====> Change the document type from '%s' to '%s'? [y/n]" % (d.type, document_type));
                    if allow_changes.lower() not in ['y','n']:
                      continue
                    else:
                      if allow_changes.lower() == 'y':
                        d.type = document_type
                        d.save()

                      break
                self.stdout.write("        - type  : %s" % d.type)
                self.stdout.write("        - refid : %s" % d.reference)
                self.stdout.write("        - id    : %s" % d.id)
                self.stdout.write("        - title : %s" % d.title)
                self.stdout.write("        - slug  : %s" % d.slug)


            # create institution Tag
            t_institution, created = Tag.objects.get_or_create(slug=slugify(affiliation), type=Tag.INSTITUTION, defaults={
                'name': affiliation
            })
            self.stdout.write("        - inst. : %s" % affiliation)

            # create year Tag
            t_year, created = Tag.objects.get_or_create(slug=slugify(tag_year), type=Tag.DATE, defaults={
                'name': tag_year
            })
            self.stdout.write("        - year  : %s" % tag_year)

            # create course Tag
            t_course, created = Tag.objects.get_or_create(slug=slugify(tag_course), type=Tag.COURSE, defaults={
                'name': tag_course
            })
            self.stdout.write("        - cour. : %s" % tag_course)

            # create tag author (if any) @todo: OMONIMS
            t_author, created = Tag.objects.get_or_create(slug=slugify(tag_author), type=Tag.AUTHOR, defaults={
                'name': tag_author
            })

            # attach affiliation to authors
            t_author.related.add(t_institution)

            self.stdout.write("        - auth. : %s" % t_author)




            d.tags.add(t_institution, t_year, t_author, t_course)
            

            self.stdout.write("\n")
    
        



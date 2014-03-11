#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, csv
from optparse import make_option
from datetime import datetime

from django.db import transaction
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from walt.models import Document, Tag
from walt.utils import unicode_dict_reader


class Command(BaseCommand):
    args = '<csv absolute path>'
    help = 'Import a list of documents from a csv file, without their authors. Csv file must be tab separated, specify the delimiter otherwise'
    option_list = BaseCommand.option_list + (
        make_option('--csv',
            action='store',
            dest='csv',
            type='string',
            default=None,
            help='csv file of documents'),
        make_option('--owner',
            action='store',
            dest='owner',
            type='string',
            default=None,
            help='owner username'),
        make_option('--delimiter',
            action='store',
            dest='delimiter',
            type='string',
            default='\t',
            help='csv cell delimiter'),
    )

    def handle(self, *args, **options):
        # set default owner if ldap is not
        self.stdout.write("\n                      *     .--.\n                           / /  `\n          +               | |\n                 '         \\ \\__,\n             *          +   '--'  *\n                 +   /\\\n    +              .'  '.   *\n           *      /======\\      +\n                 ;:.  _   ;\n                 |:. (_)  |\n                 |:.  _   |\n       +         |:. (_)  |          *\n                 ;:.      ;\n               .' \:.    /  `.\n              / .-'':._.'`-. \\\n              |/    /||\\    \\|\n        jgs _..--\"\"\"````\"\"\"--.._\n      _.-'``                    ``'-._\n    -'                                '-\n\n")
        
        if not options['csv']:
          self.stderr.write("    csv file must be specified")
          return

        if not options['owner']:
          self.stderr.write("    owner username must be privided")
          return

        if not os.path.exists( options['csv']):
          self.stderr.write("    file '\033[92m'%s not found" % options['csv'])
          return

        self.stdout.write("    opening file: '%s'" % options['csv'])
        

        
        # owner will be used as default owner; you can change it later
        try:
          owner = User.objects.get(username=options['owner'])
        except User.DoesNotExist, e:
          self.stderr.write("    user %s not found" % options['owner'])
          return
        
        self.stdout.write("    using owner: <user:%s>\n\n" % owner.username)

        f = open(options['csv'], 'rb')
        d = unicode_dict_reader(f, delimiter=options['delimiter'])

        with transaction.atomic():
          for i,row in enumerate(d):
            # document related information @todo to be improved with a documentform maybe
            
            title = row['document_title']
            abstract = row['document_abstract'] if 'document_abstract' in row else ""
            permalink = row['document_permalink']
            reference = row['document_reference']
            rating = 5.0 if row['document_rating'] == 'VRAI' else 0.0# //?????"????"

            doc, created = Document.objects.get_or_create(reference=reference, defaults={'title': title, 'owner':owner})
            doc.type = Document.REFERENCE_CONTROVERSY_WEB
            doc.save()
            print doc.title, doc.rating, created, doc.reference, doc.slug
            
            # add tags
            #tag_family, created    = Tag.objects.get_or_create(type=Tag.FAMILY, name=row['type'])
            #tag_copyright, created = Tag.objects.get_or_create(type=Tag.COPYRIGHT, name=row['model'])
            #tag_remote, created    = Tag.objects.get_or_create(type=Tag.REMOTE, name=row['local'])

            # doc, created = Document.objects.get_or_create(title=title, type=options['type'], owner=owner)
            
            # doc.permalink = permalink
            #doc.tags.add(tag_family, tag_copyright, tag_remote)
            #wordoc.save()

          self.stdout.write("    done!")
          self.stdout.write('''

                      +
       +                            *
              
                   *          


            _..--"""````"""--.._
      _.-'``                    ``'-._
    -'                                '-

          ''')
          

    
        



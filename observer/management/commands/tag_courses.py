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

from observer.models import DocumentProfile, Device, Property

from walt.models import Document, Tag, WorkingDocument
from walt.utils import unicode_dict_reader


class Command(BaseCommand):
    args = '<csv absolute path>'
    help = 'Import course tags from a csv file. Csv file must be tab separated, specify the delimiter with the delmiter param otherwise'
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
          raise CommandError("    csv file must be specified")

        if not options['owner']:
          raise CommandError("    owner username must be privided")

        if not os.path.exists( options['csv']):
          raise CommandError("    file '%s' not found" % options['csv'])

        self.stdout.write("    opening file: '%s'" % options['csv'])
        
        # owner will be used as default owner; you can change it later
        try:
          owner = User.objects.get(username=options['owner'])
        except User.DoesNotExist, e:
          raise CommandError("%s.. having username='%s'" % (e, options['owner']))
        
        self.stdout.write("    using owner: <user:%s>\n\n" % owner.username)

        f = open(options['csv'], 'rb')
        d = unicode_dict_reader(f, quotechar='"', delimiter = ',')

        with transaction.atomic():
          for i,row in enumerate(d):
            
            course_code = row['slug']
            abstract = row['title'] # title will be the course code indeed

            print abstract
            
            wod, created = WorkingDocument.objects.get_or_create(
              title=course_code,
              type=WorkingDocument.COURSE,
              defaults={'owner': owner}
            )

            wod.abstract = abstract

            for key in row:
              if key.startswith('tag_'):
                tag_value = row[key]
                tag_type = key.replace('tag_','').upper()
                tag, created = Tag.objects.get_or_create(slug=slugify(tag_value), type=Tag.INSTITUTION, defaults={
                  'name': tag_value
                })
                wod.tags.add(tag)
                print 'tag: ', key, row[key], key.startswith('tag_'), created
            
            wod.save()
            continue

          self.stdout.write("    done!")
          self.stdout.write('''

                      +
       +                            *
              
                   *          


            _..--"""````"""--.._
      _.-'``                    ``'-._
    -'                                '-

          ''')
          

    
        



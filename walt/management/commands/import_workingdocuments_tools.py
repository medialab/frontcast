#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, csv
from optparse import make_option
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from walt.models import WorkingDocument, Tag
from walt.utils import unicode_dict_reader


class Command(BaseCommand):
    args = '<csv absolute path>'
    help = 'Import a list of workingdocuments (Sequences, Tasks, Tools) from a csv file. Csv file must be comma separated'
    option_list = BaseCommand.option_list + (
        make_option('--csv',
            action='store',
            dest='csv',
            type='string',
            default=None,
            help='csv file of workingdocuments'),
        make_option('--owner',
            action='store',
            dest='owner',
            type='string',
            default=None,
            help='owner username'),
        make_option('--type',
            action='store',
            dest='type',
            type='string',
            default='',
            help='working document favourite type - cfr models.py'),
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
        
        available_type_choices = [t[0] for t in WorkingDocument.TYPE_CHOICES]

        if not options['csv']:
          self.stderr.write("    csv file must be specified")
          return

        if not options['owner']:
          self.stderr.write("    owner username must be privided")
          return

        if not os.path.exists( options['csv']):
          self.stderr.write("    file '\033[92m'%s not found" % options['csv'])
          return

        if options['type'] not in available_type_choices:  
          self.stderr.write("    available type choices have to be one of these %s" % available_type_choices)
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


        # check fields
        for i,row in enumerate(d):
          print row
          title = row['name']
          abstract = row['desc']
          permalink = row['URL']

          # add tags
          tag_family, created    = Tag.objects.get_or_create(type=Tag.FAMILY, name=row['type'])
          tag_copyright, created = Tag.objects.get_or_create(type=Tag.COPYRIGHT, name=row['model'])
          tag_remote, created    = Tag.objects.get_or_create(type=Tag.REMOTE, name=row['local'])

          wordoc, created = WorkingDocument.objects.get_or_create(title=title, type=options['type'], owner=owner)
          
          wordoc.permalink = permalink
          wordoc.abstract = abstract
          wordoc.tags.add(tag_family, tag_copyright, tag_remote)
          wordoc.save()

        self.stdout.write("    done!")
        self.stdout.write('''

                      +
       +                            *
              
                   *          


            _..--"""````"""--.._
      _.-'``                    ``'-._
    -'                                '-

        ''')
          

    
        



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

        document_translate_types = {
          'video': 'ControversyVideo',
          'site web': 'ControversyWeb',
          'website': 'ControversyWeb',
          'ebook': 'ControversyEbook',
          'controversyweb': 'ControversyWeb'
        }

        with transaction.atomic():
          for i,row in enumerate(d):
            # document related information @todo to be improved with a documentform maybe
            #document_reference,document_title,document_institution,document_year,profile_notes,document_rated
            #print i, row[parent.id (Frontcast),parent.title,parent.institution,parent.year,parent.notes,parent.rated,parent.active,parent.format,parent.URL,methodology,sources,glossary,meth_det]

            #continue
            title = row['document_title']
            abstract = row['document_abstract'] if 'document_abstract' in row else ""
            permalink = row['document_permalink']
            reference = row['document_reference']
            rating = 5.0 if row['document_rating'] == 'VRAI' else 0.0# //?????"????"
            notes = row['profile_notes']

            tag_institution = row['tag_institution']
            tag_year = row['tag_year']

            document_type = document_translate_types[row['document_type'].strip().lower()]
            

            print i, reference
            print '  ', tag_institution, tag_year

            doc, created = Document.objects.get_or_create(reference=reference, defaults={'title': title, 'owner':owner})
            if not created:
              if title != doc.title:
                print '[1]', doc.title
                print '[2]', title

                while True:
                  t = raw_input('stored document title [1] does not match with the csv one [2].  CTRL+C to quit or please type 1 or 2 to chose the right value!')
                  print t
                  if t in ('1', '2', 1, 2):
                    doc.title = doc.title if t == 1 or t == '1' else title
                    break

                print "you chosen", doc.title
            doc.type  = document_type
            doc.save()
            
            pro, created = DocumentProfile.objects.get_or_create(document=doc, defaults={'owner': owner})
            pro.notes = notes
            pro.save()

            t_institution, created = Tag.objects.get_or_create(slug=slugify(tag_institution), type=Tag.INSTITUTION, defaults={
                'name': tag_institution
            })
            
            # create year Tag
            t_year, created = Tag.objects.get_or_create(slug=slugify(tag_year), type=Tag.DATE, defaults={
                'name': tag_year
            })
            
            doc.tags.add(t_institution, t_year)
            doc.save()

            # TOOL PROPERTIES
            for device_type in Device.TYPE_CHOICES:
              if device_type[0] in row:
                devices = [t.strip() for t in row[device_type[0]].strip().split(',')] if row[device_type[0]].strip() not in (u'NONE', u'RECHECK') else []
                print 'device', device_type[0], len(devices)
                for d in devices:
                  print '  creating ', d
                  wod, created = WorkingDocument.objects.get_or_create(title=d, type=WorkingDocument.TOOL, owner=owner)
                  print '  created ', d
                  print '  connectiong ', d, device_type[0][:12]
                  device, created = Device.objects.get_or_create(document=doc, working_document=wod, type=device_type[0][:12])
                  print '  connected ', d

            # NORMAL PROPERTIES
            for property_type in Property.TYPE_CHOICES:
              if property_type[0] in row:
                property_name = property_type[0]
                has_property = True if row[property_type[0]].strip() == 'VRAI' else False
                if has_property:
                  try:
                    prop = Property.objects.get(type=property_name[:12])
                  except Property.DoesNotExist, e:
                    raise CommandError("%s.. having type='%s'" % (e, property_name[:12]))
                  #print 'property', property_name, has_property
                  pro.properties.add(prop)
                  pro.save()

            #MULTICHOICE PROPERTIES (to be translated!)
            meth_details = [t.strip() for t in row['meth_details'].strip().split(',')] if row['meth_details'].strip() not in (u'NONE', u'RECHECK') else []
            print 'meth_details',meth_details
            if reference == 'uniman-hum3-2011-0004':
              break

          self.stdout.write("    done!")
          self.stdout.write('''

                      +
       +                            *
              
                   *          


            _..--"""````"""--.._
      _.-'``                    ``'-._
    -'                                '-

          ''')
          

    
        



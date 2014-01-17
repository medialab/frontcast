import os, csv
from optparse import make_option

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from walt.models import Document, Tag
from walt.utils import unicode_dict_reader


class Command(BaseCommand):
    args = ''
    help = 'Build a SQLITE search index with FTS3 by adding a virtual table or dropping it if it exists'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        # set default owner if ldap is not
        self.stdout.write("\n------------------------------------------\n\n    welcome to import_reference script\n    ==================================\n\n\n\n")
        
        self.stdout.write("\n")
    
        



from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.core import serializers
from django.apps import apps
from django.db import connection
import os
import logging

from customer.models import Customer

# logger = logging.getlogger(__name__)

APPS_TO_BACKUP=[
    # 'core',
    'customer',
    # 'product',
    # 'order',
    # 'landing',
]


class Command(BaseCommand):

    help = 'Creates a backup files for db of above apps'

    def handle(self, *args, **options):
        customers = Customer.objects.all()
        serialized_data = serializers.serialize('json', customers)
        with open('customers.json', 'w') as file:
            file.write(serialized_data)
        # backup_filename = '/home/sasha/PycharmProjects/ecommerce/backup.json'
        # try:
        #     with open(backup_filename, 'w') as f:
        #         call_command('dumpdata', 'customer', stdout=f)
        # except Exception as e:
        #     print(e)






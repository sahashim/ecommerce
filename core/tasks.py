
from ecommerce.celery import app
from celery import Celery
from celery import shared_task
from django.core.management import call_command

@shared_task()
def backup_database():
    call_command('backup_db')
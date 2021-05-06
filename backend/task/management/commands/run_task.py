from django.core.management.base import BaseCommand
from module.eaeo import schedule as sch
from module.eaeo import constant as mcs
import threading

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        if mcs.auto_sync:
            th = threading.Thread(target=sch.instagram_sync_scheduler())
            th.start()

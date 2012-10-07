from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from poscore.models import Corporation
from eveapi import EVEAPIConnection, Error

class Command(BaseCommand):
    args = ''
    help = 'Updates all corporations from the EVE API'

    def handle(self, *args, **options):
        api = EVEAPIConnection()

        self.stdout.write('Updating %d corporations... ' % Corporation.objects.count())
        with transaction.commit_on_success():
            for corp in Corporation.objects.all():
                print corp.pk
                try:
                    res = api.corp.CorporationSheet(corporationID=corp.pk)
                except Error:
                    continue
                corp.name = res.corporationName
                corp.ticker = res.ticker
                if hasattr(res, 'allianceID'):
                    corp.alliance_id = int(res.allianceID)
                corp.save()
        self.stdout.write('Done\n')
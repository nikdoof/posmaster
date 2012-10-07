from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from poscore.models import Alliance, Corporation
from eveapi import EVEAPIConnection

class Command(BaseCommand):
    args = ''
    help = 'Updates alliances from the EVE API'

    def handle(self, *args, **options):
        api = EVEAPIConnection()

        alliance_list = api.eve.AllianceList().alliances
        print 'Updating %d alliances... ' % len(alliance_list)
        with transaction.commit_on_success():
            for alliance in alliance_list:
                allobj, created = Alliance.objects.get_or_create(pk=alliance.allianceID)
                allobj.name = alliance.name
                allobj.save()
                corp_ids = [x.corporationID for x in alliance.memberCorporations]
                Corporation.objects.exclude(pk__in=corp_ids).update(alliance=None)
                Corporation.objects.filter(pk__in=corp_ids).update(alliance=allobj)
        print 'Done'
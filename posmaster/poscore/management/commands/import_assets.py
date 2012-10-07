from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import utc, now
from poscore.models import APIKey, Location, System, Moon, Tower, Corporation, InSpaceObject
from eveapi import EVEAPIConnection

class Command(BaseCommand):
    args = ''
    help = 'Updates the in-space assets from the EVE API'

    def handle(self, *args, **options):
        api = EVEAPIConnection()

        for key in APIKey.objects.filter(active=True):
            auth = key.auth(api)

            assets = auth.corp.AssetList().assets
            for asset in assets:
                if int(asset.flag) > 0:
                    continue

                try:
                    obj = InSpaceObject.objects.get(pk=asset.itemID)
                except InSpaceObject.DoesNotExist:
                    obj = InSpaceObject(pk=asset.itemID, type_id=asset.typeID, system_id=asset.locationID)
                obj.save()

            print "Importing POSes"
            starbases = auth.corp.StarbaseList().starbases
            for base in starbases:
                owner, created = Corporation.objects.get_or_create(pk=base.standingOwnerID)
                system, created = System.objects.get_or_create(pk=base.locationID)
                moon, created = Moon.objects.get_or_create(pk=base.moonID)

                try:
                    twr = Tower.objects.get(pk=base.itemID)
                except Tower.DoesNotExist:
                    twr = Tower(pk=base.itemID, type_id=base.typeID, system_id=base.locationID, moon_id=base.moonID, name="Tower %s" % base.itemID, owner=owner)
                twr.state = base.state
                twr.state_datetime = datetime.fromtimestamp(base.stateTimestamp, utc)
                twr.online_datetime = datetime.fromtimestamp(base.onlineTimestamp, utc)
                twr.save()

            print "Flagging POSes missing from the API"
            tower_ids = [x.itemID for x in starbases]
            Tower.objects.exclude(pk__in=tower_ids).update(state=Tower.STATE_MISSING)
            print "Done"

            # Grab locations
            twr_dict = {}
            for twr in InSpaceObject.objects.filter(x=None):
                twr_dict[twr.pk] = twr
            keys = twr_dict.keys()

            while len(keys) > 0:
                if len(keys) < 250:
                    call = keys
                    keys = []
                else:
                    call = keys[:250]
                    keys = keys[251:]

                id_list = ','.join([str(x) for x in call])
                print "Updating %d locations" % len(call)
                locations = auth.corp.Locations(IDs=id_list).locations
                for loc in locations:
                    twr = twr_dict.get(int(loc.itemID), None)
                    if not twr:
                        continue
                    twr.name = loc.itemName
                    twr.x = loc.x
                    twr.y = loc.y
                    twr.z = loc.z
                    twr.save()



        self.stdout.write('Done\n')
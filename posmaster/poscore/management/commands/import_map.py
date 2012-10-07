from __future__ import division
import sqlite3

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from poscore.models import Region, Constellation, System, Planet, Moon

class Command(BaseCommand):
    args = '<map csv>'
    help = 'Imports the EVE Map from a CSV dump of the SDE table mapDenormalized'

    def handle(self, *args, **options):

        # Connect to the sqlite3 DB
        db = sqlite3.connect(args[0])
        cur = db.cursor()
        
        objs = []
        
        # eveUnits
        print "Importing mapDenormalize..."
        cur.execute("""SELECT itemID, typeID, groupID, solarSystemID, constellationID, regionID, orbitID, x, y, z, itemName FROM mapDenormalize WHERE typeID in (3, 4, 5, 14) OR groupID = 7""")
        for row in cur.fetchall():
            id, type, group, solarid, constellationid, regionid, orbitid, x, y, z, name = row    
            
            if int(type) == 3:
                objs.append(Region(pk=id, name=name, x=0, y=0, z=0))
            elif int(type) == 4:
                objs.append(Constellation(pk=id, name=name, region_id=regionid,  x=0, y=0, z=0))
            elif int(type) == 5:
                objs.append(System(pk=id, name=name, constellation_id=constellationid, x=0, y=0, z=0))
            elif int(group) == 7:
                objs.append(Planet(pk=id, name=name, system_id=solarid, x=x, y=y, z=z))
            elif int(type) == 14:
                objs.append(Moon(pk=id, name=name, planet_id=orbitid, x=x, y=y, z=z))
        print "Done"
        # Dump to DB
        
        print 'Processing %d objects for commiting...' % len(objs)
        with transaction.commit_on_success():
            for i, x in enumerate(objs, start=1):
                if i % 1000 == 0: print "%d/%d (%d%%)" % (i, len(objs), round(i/len(objs) * 100))
                x.save()
        print 'Commited'

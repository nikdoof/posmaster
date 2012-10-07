import sqlite3
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from poscore.models.types import TypeCategory, TypeGroup, Type, AttributeType, UnitType, TypeAttribute

class Command(BaseCommand):
    args = '<SDE SqliteDB>'
    help = 'Imports type data from the EVE SDE'

    def handle(self, *args, **options):

        # Connect to the sqlite3 DB
        db = sqlite3.connect(args[0])
        cur = db.cursor()
        
        objs = []
        
        # eveUnits
        print "Importing eveUnits..."
        cur.execute("""SELECT unitID, unitName, displayName FROM eveUnits""")
        for row in cur.fetchall():
            objs.append(UnitType(pk=row[0], name=row[1], display_name=row[2] or ''))
            
        # dgmAttributeTypes
        print "Importing dgmAttributeTypes..."
        cur.execute("""SELECT attributeID, attributeName, displayName, unitID FROM dgmAttributeTypes""")
        for row in cur.fetchall():
            objs.append(AttributeType(pk=row[0], name=row[1], display_name=row[2] or '', unit_id=row[3]))
            
        # invCategories
        print "Importing invCategories..."
        cur.execute("""SELECT categoryID, categoryName FROM invCategories""")
        for row in cur.fetchall():
            objs.append(TypeCategory(pk=row[0], name=row[1]))
            
        # invGroups
        print "Importing invGroups..."
        cur.execute("""SELECT groupID, groupName, categoryID FROM invGroups""")
        for row in cur.fetchall():
            objs.append(TypeGroup(pk=row[0], name=row[1], category_id=row[2]))
            
        # invTypes
        print "Importing invTypes..."
        cur.execute("""SELECT typeID, typeName, capacity, groupID FROM invTypes""")
        for row in cur.fetchall():
            objs.append(Type(pk=row[0], name="".join(i for i in row[1] if ord(i)<128), capacity=row[2], group_id=row[3]))

        # dgmTypeAttributes
        print "Importing dgmTypeAttributes..."
        cur.execute("""SELECT typeID, attributeID, valueInt, valueFloat FROM dgmTypeAttributes""")
        for row in cur.fetchall():
             objs.append(TypeAttribute(type_id=row[0], attribute_id=row[1], valueint=row[2], valuefloat=row[3]))
            
        # Dump to DB
        print 'Processing %d objects for commiting...' % len(objs)
        with transaction.commit_on_success():
            for i, x in enumerate(objs, start=1):
                if i % 1000 == 0: print "%d/%d (%d%%)" % (i, len(objs), round(i/len(objs) * 100))
                x.save()
        print 'Commited'

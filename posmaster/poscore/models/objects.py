from math import sqrt
from django.db import models
from django.core.urlresolvers import reverse_lazy

from poscore.app_defines import *
from .types import Type
from .owners import Owner
from .locations import System, Moon

class InSpaceObject(models.Model):
    """Represents a object in space"""
    id = models.BigIntegerField('Object ID', primary_key=True)
    type = models.ForeignKey(Type, related_name='assets')
    owner = models.ForeignKey(Owner, related_name='assets', null=True)
    system = models.ForeignKey(System, related_name='assets')
    x = models.BigIntegerField('X Location', null=True)
    y = models.BigIntegerField('Y Location', null=True)
    z = models.BigIntegerField('Z Location', null=True)

    @staticmethod
    def _calc_distance(sys1, sys2):
        """Calculate the distance between two sets of 3d coordinates"""
        return sqrt((sys1.x-sys2.x)**2+(sys1.y-sys2.y)**2+(sys1.z-sys2.z)**2) / 1000

    def distance(self, object):
        """Calculate the distance between this object and another"""
        return InSpaceObject._calc_distance(self, object)

    def nearby_objects(self, distance):
        """Returns a queryset of nearby objects"""
        systemobjs = self.system.assets.exclude(pk=self.pk)
        outobj = []
        for obj in systemobjs:
            if self.distance(obj) <= distance:
                outobj.append(obj)
        return outobj

    class Meta:
            app_label = 'poscore'

    def __unicode__(self):
        return '%s (%s)' % (self.type.name, self.system.name)


class Tower(InSpaceObject):
    """Tower or POS Tower in space"""

    STATE_UNANCHORED = 0
    STATE_OFFLINE = 1
    STATE_ONLINING = 2
    STATE_REINFORCED = 3
    STATE_ONLINE = 4
    STATE_MISSING = 5

    STATE_CHOICES = (
        (STATE_UNANCHORED, 'Unanchored'),
        (STATE_OFFLINE, 'Offline'),
        (STATE_ONLINING, 'Onlining'),
        (STATE_REINFORCED, 'Reinforced'),
        (STATE_ONLINE, 'Online'),
        (STATE_MISSING, 'Missing'),
    )
    
    SIZE_SMALL = 1
    SIZE_MEDIUM = 2
    SIZE_LARGE = 3
    
    SIZE_CHOICES = (
        (SIZE_SMALL, 'Small POS'),
        (SIZE_MEDIUM, 'Medium POS'),
        (SIZE_LARGE, 'Large POS'),
    )

    name = models.CharField('Name', max_length=200)
    state = models.PositiveIntegerField('State', choices=STATE_CHOICES, default=STATE_UNANCHORED)
    moon = models.ForeignKey(Moon, related_name='structures')

    state_datetime = models.DateTimeField('State Date/Time')
    online_datetime = models.DateTimeField('Online Date/Time')
    updated_datetime = models.DateTimeField('Last Update Date/Time', auto_now=True)

    def modules(self):
        """Find modules based on the tower's type attributes"""
        if not hasattr(self, '_max_distance'):
            self._max_distance = self.type.attributes.get(attribute_id=ATTRIBUTE_MAX_STRUCTURE_DISTANCE).value / 1000
        return self.nearby_objects(self._max_distance)
        
    def power_usage(self):
        total = 0
        for mod in self.modules():
            total += mod.type.attributes.get(attribute_id=30).value
        return total
            
    def cpu_usage(self):
        total = 0
        for mod in self.modules():
            total += mod.type.attributes.get(attribute_id=50).value
        return total
        
    @property
    def size(self):
        """Returns the size of the POS based on its type"""
        if self.type.pk in []:
            return SIZE_SMALL
        elif self.type.pk in []:
            return SIZE_MEDIUM
        else:
            return SIZE_LARGE
            
    def get_size_display(self):
        size = self.size
        for i, name in Tower.SIZE_CHOICE:
            if i == size:
                return name

    class Meta:
        app_label = 'poscore'

    def get_absolute_url(self):
        return reverse_lazy('tower-detail', kwargs={'pk': self.pk})
        
    def save(self, *args, **kwargs):
        if not self.type.group_id in TYPEGROUP_TOWERS:
            raise ValueError('You can\'t create a Tower with a non-tower typeID: %d - %s' % (self.type.pk, self.type.name))
        return super(Tower, self).save(*args, **kwargs)


class Fuel(models.Model):

    tower = models.ForeignKey(Tower, related_name='fuel')
    resource = models.ForeignKey(Type, related_name='+', limit_choices_to={'group__pk__in': TYPEGROUP_FUEL})
    level = models.PositiveIntegerField('Resource Level')

    updated_datetime = models.DateTimeField('Last Update Date/Time', auto_now=True)

    class Meta:
        app_label = 'poscore'


class Silo(InSpaceObject):

    resource = models.ForeignKey(Type, related_name='+', limit_choices_to={'group__category__pk': 4})
    level = models.PositiveIntegerField('Resource Level', default=0)

    emptied_datetime = models.DateTimeField('Last Emptied Date/Time')
    updated_datetime = models.DateTimeField('Last Update Date/Time', auto_now=True)

    class Meta:
        app_label = 'poscore'


class JumpBridge(InSpaceObject):

    level = models.PositiveIntegerField('Liquid Ozone Level', default=0)
    updated_datetime = models.DateTimeField('Last Update Date/Time', auto_now=True)

    class Meta:
        app_label = 'poscore'
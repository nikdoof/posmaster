from django.db import models

class Owner(models.Model):
    id = models.BigIntegerField('Owner ID', primary_key=True)
    name = models.CharField('Owner Name', max_length=200)

    class Meta:
        app_label = 'poscore'

    def __unicode__(self):
        return self.name

class Alliance(Owner):

    class Meta:
        app_label = 'poscore'

class Corporation(Owner):
    """Represents a EVE Corporation """
    alliance = models.ForeignKey(Alliance, related_name='corporations', null=True)

    class Meta:
        app_label = 'poscore'
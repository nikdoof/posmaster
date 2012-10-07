from django.conf import settings
from django.db import models

class TypeCategory(models.Model):
    id = models.BigIntegerField('Type Category ID', primary_key=True)
    name = models.CharField('Type Category Name', max_length=200)

    class Meta:
        app_label = 'poscore'
        
    def __unicode__(self):
        return self.name

class TypeGroup(models.Model):
    id = models.BigIntegerField('Type Group ID', primary_key=True)
    category = models.ForeignKey(TypeCategory, related_name='groups')
    name = models.CharField('Type Group Name', max_length=200)

    class Meta:
        app_label = 'poscore'
        
    def __unicode__(self):
        return self.name

class Type(models.Model):
    """Represents a EVE InvType"""
    id = models.BigIntegerField('Type ID', primary_key=True)
    group = models.ForeignKey(TypeGroup, related_name='types')
    name = models.CharField('Type Name', max_length=200)
    capacity = models.BigIntegerField('Capacity')

    @property
    def image(self):
        return '%s/Type/%s_%s.png' % (getattr(settings, 'EVE_IMAGESERVER_URL', 'https://image.eveonline.com'), self.pk, getattr(settings, 'EVE_IMAGESERVER_TYPESIZE', 64))
        
    def render(self, size):
        if size % 32:
            raise ValueError('Size isn\'t a multiple of 32')
        if size > 512:
            raise ValueError('Size is too large (max 512px)')
        return '%s/Render/%s_%s.png' % (getattr(settings, 'EVE_IMAGESERVER_URL', 'https://image.eveonline.com'), self.pk, size)

    @property
    def attributes_list(self):
        return [(attr.attribute.display_name or attr.attribute.name, attr.get_value_display()) for attr in self.attributes.all()]
        
    class Meta:
        app_label = 'poscore'

    def __unicode__(self):
        return self.name
 

class UnitType(models.Model):

    id = models.BigIntegerField('Unit ID', primary_key=True)
    name = models.CharField('Unit Name', max_length=200)
    display_name = models.CharField('Display Name', max_length=200)   

    class Meta:
        app_label = 'poscore'

    def __unicode__(self):
        return self.name    
 
class AttributeType(models.Model):

    id = models.BigIntegerField('Attribute ID', primary_key=True)
    name = models.CharField('Attribute Name', max_length=200)
    display_name = models.CharField('Display Name', max_length=200)
    unit = models.ForeignKey(UnitType, related_name='+', null=True)
    
    class Meta:
        app_label = 'poscore'

    def __unicode__(self):
        return self.name
        
class TypeAttribute(models.Model):

    type = models.ForeignKey(Type, related_name='attributes')
    attribute = models.ForeignKey(AttributeType, related_name='+')
    valueint = models.BigIntegerField('Int Value', null=True)
    valuefloat = models.FloatField('Float Value', null=True)
    
    @property
    def value(self):
        return self.valuefloat or self.valueint
        
    def get_value_display(self):
        if self.attribute.unit:
            return u'%d%s' % (self.value, self.attribute.unit.display_name)
        return self.value
    
    class Meta:
        app_label = 'poscore'

    def __unicode__(self):
        return self.attribute.name
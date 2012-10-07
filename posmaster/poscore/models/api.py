from django.db import models

class APIKey(models.Model):

    keyid = models.BigIntegerField('Key ID', primary_key=True)
    vcode = models.CharField('Verification Code', max_length=64)
    active = models.BooleanField('Active', default=True)

    def auth(self, api):
        return api.auth(keyID=self.keyid, vCode=self.vcode)

    class Meta:
            app_label = 'poscore'
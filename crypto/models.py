import json
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Wallet(models.Model):
    
    balance = models.IntegerField()
    uid = models.CharField(max_length=30)
    public_key = models.CharField(max_length=30)
    private_key = models.CharField(max_length=30)
    wallet_address = models.CharField(max_length=30)
    date_created = models.DateField(auto_now_add=True)
    #cards = ArrayField(models.CharField(max_length=30,blank=True) ,size=8,)
    #payees = ArrayField(models.CharField(max_length=30), default=[])
    #transactions = ArrayField(models.CharField(max_length=30), default=[])

    class Meta:
        ordering = ['-date_created']

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __str__(self):
        return self.uid



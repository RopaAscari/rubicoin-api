import json
from django.db import models

class Verification(object):
    def __init__(self, code, date):
        self.code = code
        self.date = date

class User(models.Model):    

    email = models.CharField(max_length=13)
    password = models.CharField(max_length=13) 
    last_name = models.CharField(max_length=100)  
    first_name = models.CharField(max_length=150)    
    phone_number = models.CharField(max_length=13)
    phone_number = models.CharField(max_length=13)
    date_created = models.DateField(auto_now_add=True)
    wallet_connected = models.BooleanField(default=False)
    mining_rig_connected = models.BooleanField(default=False)
    verify_code = models.CharField(max_length=13, default="")
    verify_date = models.CharField(max_length=13, default="")

    class Meta:
        ordering = ['-date_created']
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __str__(self):
        return self.first_name


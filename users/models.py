import json
from django.db import models

class Verification(object):
    def __init__(self, code, date):
        self.code = code
        self.date = date

class Country(models.Model):
    id = models.IntegerField(primary_key=True)   
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __str__(self):
        return self.id
    
class User(models.Model):   
    #_id = models.ObjectIdField()
    id = models.IntegerField(primary_key=True, unique=True) 
    terms_agreed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    email = models.CharField(max_length=13, default="") 
    wallet_connected = models.BooleanField(default=False)
    province = models.CharField(max_length=20, default="")
    password = models.CharField(max_length=13, default="")
    
    last_name = models.CharField(max_length=100, default="")  
    first_name = models.CharField(max_length=150, default="")
    ip_address = models.CharField(max_length=20, default="")
    mining_rig_connected = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=13, default="") 
    verify_code = models.CharField(max_length=13, default=None)
    verify_date = models.CharField(max_length=13, default=None)
    country_code = models.CharField(max_length=13, default="")
    country_name = models.CharField(max_length=13, default="")
    messaging_token = models.CharField(max_length=20,default=None)
    #models.ForeignKey(Country, on_delete=models.CASCADE)
    class Meta:
        ordering = ['-date_created']
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __str__(self):
        return self.first_name


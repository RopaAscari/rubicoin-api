import json
from django.db import models

class Card(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    uid = models.CharField(max_length=30)
    issuer = models.CharField(max_length=10)
    card_number = models.CharField(max_length=16)    
    card_holder_name = models.CharField(max_length=150)    
    cvc = models.CharField(max_length=150)    
    address = models.CharField(max_length=13)
    city = models.CharField(max_length=13)
    expiry_date = models.CharField(max_length=100)  
    province = models.CharField(max_length=13)
    country = models.CharField(max_length=13)
    postal_code = models.CharField(max_length=13)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __str__(self):
        return self.card_number
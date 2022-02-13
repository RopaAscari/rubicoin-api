import json
from djongo import models

# Create your models here.
class Notification(models.Model):
    type = models.CharField(max_length=10)
    message = models.CharField(max_length=20)
    user_id = models.CharField(max_length=10)
    is_unread = models.BooleanField(default=True)
    avatar = models.CharField(max_length=10, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.IntegerField(primary_key=True, unique=True)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def __str__(self):
        return self.user_id
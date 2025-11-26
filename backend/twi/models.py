from django.db import models
from django.core import serializers
# Create your models here.
        
class Post(models.Model):
    post_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return (serializers.serialize('json', [ self ]))


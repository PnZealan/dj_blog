from __future__ import unicode_literals

from django.db import models

# Create your models here.
class article_list(models.Model):
    id =  models.AutoField(primary_key = True)
    time = models.DateField( auto_now_add=True)
    title = models.CharField( max_length = 50)
    content = models.TextField()
    def __unicode__(self):
        return self.title

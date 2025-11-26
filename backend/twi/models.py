from django.db import models
# Create your models here.
        
class Post(models.Model):
    post_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return '{"id":"%s","post_text":"%s","pub_date":"%s"}' % (self.id, self.post_text, self.pub_date)
        
    def to_json(self):
        return {
            'id': self.id,
            'post_text': self.post_text,
            'pub_date': self.pub_date
        }

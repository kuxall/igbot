from django.db import models

class InstagramUser(models.Model):
    title = models.CharField(max_length=255)
    profile_link = models.URLField()
    profile_id = models.CharField(max_length=255)
    message = models.TextField()
    
    def __str__(self):
        return self.title

from django.db import models

from .rareuser import RareUser

class Comment(models.Model):
        
        post = models.ForeignKey("Post", on_delete=models.CASCADE)
        author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
        content = models.CharField(max_length=250)
        created_on = models.DateTimeField(auto_now=False)
        
        
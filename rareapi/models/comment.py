from django.db import models

class Comment(models.Model):
        
        post = models.ForeignKey("Post", on_delete=models.CASCADE)
        author = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="comments")
        content = models.CharField(max_length=250)
        created_on = models.DateTimeField(auto_now=True)
        
        
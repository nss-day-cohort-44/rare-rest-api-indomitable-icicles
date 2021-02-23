from django.db import models


class Post(models.Model):
    rare_user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=55)
    publication_date = models.DateField()
    content = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="posts", height_field=None, width_field=None, max_length=None)
    approved = models.BooleanField(default=True)
    
    @property
    def posttags(self):
        return self.__posttags

    @posttags.setter
    def posttags(self, value):
        self.__posttags = value

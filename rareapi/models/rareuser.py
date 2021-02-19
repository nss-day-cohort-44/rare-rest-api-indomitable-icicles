from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateField
from django.db.models.fields.files import ImageField



class RareUser(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    profile_image_url = models.ImageField(upload_to='Games', height_field=None, width_field=None, max_length=None)
    created_on = models.DateTimeField(auto_now_add=True)
    active =  models.BooleanField(default=True)
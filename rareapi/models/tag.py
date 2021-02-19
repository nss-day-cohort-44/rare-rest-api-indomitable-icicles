from django.db import models

class Tag(models.Model):
    label = models.CharField(max_length=75)

    # @property
    # def tagged(self):
    #     return self.__joined

    # @tagged.setter
    # def tagged(self, value):
    #     self.__tagged = value
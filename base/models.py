from django.db import models

# Create your models here.
class Text(models.Model):
    checkText = models.TextField(null=True, blank=True)



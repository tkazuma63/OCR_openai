from django.db import models

# Create your models here.

class Document(models.Model):
    image = models.ImageField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
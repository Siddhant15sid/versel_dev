from django.db import models
import uuid 

def create_uid():
    return str(uuid.uuid4())

# Create your models here.
class stock(models.Model): 
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=400)


from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.Charfield(max_length=100)
    date_of_birth = models.DateField()
    excel_file = models.FileField(upload_to='uploads/')
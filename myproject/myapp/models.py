from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.dob}"
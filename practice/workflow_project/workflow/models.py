from django.db import models

# Create your models here.
class Workflow(models.Model)
    name = models.CharField(max_lenghth=100)

class Step(models.Model):
    name = models.CharField(max_length=100)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
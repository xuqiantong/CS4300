from django.db import models

# Create your models here.

# Query: Model representing the user's input when querying the system
class Query(models.Model):
    TOLERANCE_CHOICES = (
        ('N', 'No Tolerance'),
        ('L', 'Low Tolerance'),
        ('M', 'Mild Tolerance'),
        ('H', 'High Tolerance')
    )
    is_recreational = models.BooleanField()
    conditions = models.CharField(max_length=250)
    undesired_effects = models.CharField(max_length=250)
    tolerance = models.CharField(max_length=1, choices=TOLERANCE_CHOICES)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()

    def get_results():
        pass
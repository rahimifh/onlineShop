from django.db import models

# Create your models here.

class product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length= 10)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    

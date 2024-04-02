from django.db import models

# Create your models here.

class product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length= 10)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField()

    def __str__(self) -> str:
        return f"{self.name} _ {self.id}"

    

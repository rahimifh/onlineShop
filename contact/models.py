from django.db import models


class ContactUs(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

class Contact(models.Model):
    phone_number = models.CharField(max_length=11)
    email = models.EmailField()
    address = models.TextField()
    telegram = models.CharField(max_length=50)
    whatsapp = models.CharField(max_length=50)
    instagram = models.CharField(max_length=50)
    eitaa = models.CharField(max_length=50)

    def __str__(self):
        return self.email

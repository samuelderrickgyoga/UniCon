from django.db import models

# Create your models here.
class Biodata(models.Model):
    def __init__(self, name, age, address, phone_number, email, password, gender, date_of_birth):
        self.name = name
        self.age = age
        self.address = address
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.gender = gender
        self.date_of_birth = date_of_birth
    
    name = models.CharField(max_length=20)
    age = models.IntegerField()
    address = models.CharField(max_length=50)
    phone_number = models.Integer()
    email = models.EmailField(max_length=50)
    password = models.CharField(max_lenght=12)
    gender = models.CharField(max_length=6)
    date_of_birth = models.DateField(max_length=8)
    
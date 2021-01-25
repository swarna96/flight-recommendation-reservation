from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
# Create your models here.


class Flight(models.Model):
    Economy='eco'
    First_class='f_class'
    Business='Business'
    Travel_class = [

    ('Economy', 'Economy'),
    ('First_class', 'First_class'),
    ('Business', 'Business'),
    ]

    Flight = models.CharField(max_length=50)
    From_place = models.CharField(max_length=30)
    To_place = models.CharField(max_length=30)
    Date = models.DateField()
    Depart_at_from = models.TimeField()
    Arrival_at_to = models.TimeField()
    Travel_class= models.CharField(max_length = 12,choices = Travel_class,default = Economy )
    Total_seat = models.IntegerField()
    Available = models.IntegerField()

    Rate = models.IntegerField()
    
    

    def __str__(self):
        return str(self.Flight)+str(self.From_place)+str(self.To_place) +str(self.Date)+ str(self.Depart_at_from) + str(self.Arrival_at_to) + str(self.Travel_class) + str(self.Total_seat) + str(self.Available) + str(self.Rate)



class Input_Data(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    user_name=models.CharField(max_length=50,null=True)
    airline_name=models.CharField(max_length=50)
    overall_rating=models.IntegerField(validators=[MaxValueValidator(10)])


    def __str__(self):
        return str(self.user_id)+str(self.user_name)+str(self.airline_name)+str(self.overall_rating)

class Contact(models.Model):
    first_name=models.CharField(max_length=50,null=True)
    last_name=models.CharField(max_length=50,null=True)
    email_id=models.EmailField(max_length=254,null=True)
    country=models.CharField(max_length=50,null=True)
    subject=models.TextField()
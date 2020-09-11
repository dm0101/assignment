from django.db import models
from django.contrib.auth.models import(
	AbstractUser,
	)
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(max_length = 16,null=True,blank=True,default=None)
    last_name = models.CharField(max_length = 16,null=True,blank=True,default=None)
    username = models.CharField(max_length = 16,unique=True)

    def __str__(self):
        return self.username

class City(models.Model):
    name = models.CharField(max_length = 16,null=True,blank=True,default=None,unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length = 16,null=True,blank=True,default=None,unique=True)
    city = models.ManyToManyField(City)

    def __str__(self):
        return self.name

class Showtime(models.Model):
    movie = models.ForeignKey(Movie,to_field= 'name',on_delete = models.DO_NOTHING,null=True,blank=True,default=None)
    time = models.TimeField(auto_now=False, auto_now_add=False)
    seats = models.IntegerField()

    def __str__(self):
        return str(self.time)

class Cinema(models.Model):
    name = models.CharField(max_length = 16,null=True,blank=True,default=None,unique=True)
    movie = ArrayField(models.CharField(max_length=200,unique=True), default=list)

    def __str__(self):
        return self.name

class Booking(models.Model):
    showtime = models.ForeignKey(Showtime,on_delete = models.DO_NOTHING,null=True,blank=True,default=None)
    user = models.ForeignKey(User,to_field= 'username',on_delete = models.DO_NOTHING,null=True,blank=True,default=None)
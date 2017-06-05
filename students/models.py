from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Students(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHERS = 'O'
    GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others')
        ]
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    email = models.EmailField()
    date_of_birth = models.DateField(blank = False, null = False)
    gender = models.CharField(max_length = 2, choices = GENDER, default = MALE)
    password = models.CharField(max_length = 100)
    profile_pic = models.ImageField(upload_to = 'profile_pics', null = False)
    date_created = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        fullname = self.first_name + " " + self.last_name
        return fullname
    class Meta:
        verbose_name_plural = 'Students'
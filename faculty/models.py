from django.db import models
from datetime import date

# Create your models here.


COURSES = (('SE', 'Software Engineering'),
            ('BIS', 'Business Information Systems'),
            ('DBMS', 'Database Management Systems'),
            ('TC', 'Technical Communication'),
            ('CN', 'Computer Networks'),
            ('LP', 'Language Processors'),
            )

class Register(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    factid = models.IntegerField(null=True)
    course= models.CharField(max_length=4,choices=COURSES,unique=True)
    count = models.IntegerField(default=0)
    password = models.CharField(max_length=20)
    approval = models.BooleanField(default=False)

    def __str__(self):
        return  self.username


class Attendance_sheet(models.Model):
    factid = models.IntegerField()
    course = models.CharField(max_length=30)
    date = models.DateField(default=date.today)
    sid = models.IntegerField()








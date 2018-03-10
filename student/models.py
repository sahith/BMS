from django.db import models

# Create your models here.

COURSES = (('SE', 'Software Engineering'),
            ('BIS', 'Business Information Systems'),
            ('DBMS', 'Database Management Systems'),
            ('TC', 'Technical Communication'),
            ('CN', 'Computer Networks'),
            ('LP', 'Language Processors'),
            )


class RegisterStudent(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    studid = models.IntegerField(unique=True)
    password = models.CharField(max_length=20)
    bluetooth_addr = models.CharField(max_length=30, unique=True)
    approval = models.BooleanField(default=False)

    def __str__(self):
        return  self.username


class StudentCourses(models.Model):
    studentid = models.ForeignKey(RegisterStudent,on_delete=models.CASCADE)
    course = models.CharField(max_length=50)

    def __str__(self):
        return  self.course



from django.db import models

class DateOfBirth(models.Model):
    year  = models.DateField()
    month = models.DateField()
    day   = models.DateField()

    class Meta:
        db_table = 'date_of_births'

class Gender(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'genders'

    def __str__(self):
        return self.name

class PhoneNumber(models.Model):
    country_code =  models.CharField(max_length=20)
    phone_number = models.CharField(max_length = 20)

    class Meta:
        db_table = 'phone_numbers'

    def __str__(self):
        return self.phone_number


class User(models.Model):
     username      = models.CharField(max_length=20)
     name          = models.CharField(max_length=30)
     password      = models.CharField(max_length=200)
     date_of_birth = models.ForeignKey(DateOfBirth, on_delete=models.CASCADE)
     gender        = models.ForeignKey(Gender, on_delete=models.CASCADE)
     phone_number  = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE)

     def __str__(self):
         return self.username
     class Meta:
         db_table = 'users'

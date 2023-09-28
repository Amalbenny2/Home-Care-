from django.contrib.auth.models import AbstractUser
from django.db import models



class Login(AbstractUser):
    is_Customer=models.BooleanField(default=False)
    is_Worker = models.BooleanField(default=False)


class Services(models.Model):
    name = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return self.name


# Worker model
class Worker(models.Model):
    user = models.ForeignKey(Login,on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True,null=True)
    address = models.TextField()
    phone_number = models.IntegerField()
    location = models.TextField()
    image = models.ImageField(upload_to='images/',null=True)

    def __str__(self):
        return self.name

class Worker_schedule(models.Model):
    user=models.ForeignKey(Worker,on_delete=models.CASCADE)
    start_time=models.TimeField('start_time')
    end_time=models.TimeField('end_time')
    date=models.DateField()




# Customer models
class Customer(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE,)
    name = models.CharField(max_length=30,unique=True,null=True)
    address = models.TextField()
    phone_number = models.IntegerField()
    location = models.TextField()
    # image = models.ImageField(upload_to='images/', null=True)
    def __str__(self):
        return self.name




class Appointment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    # Worker = models.ForeignKey(Worker,on_delete=models.CASCADE,null=True,blank=True)
    Worker_schedule = models.ForeignKey(Worker_schedule, on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(default=0)



# class Appointment(models.Model):
#     user_name = models.ForeignKey(Register, on_delete=models.CASCADE, related_name='Register.name+')
#     physician = models.ForeignKey(Register, on_delete=models.CASCADE)
#     date = models.DateField()
#     status = models.IntegerField(default=0)

# #
# # Complaint models
class Complaint(models.Model):
    user = models.ForeignKey(Login, on_delete=models.CASCADE,)
    description = models.TextField()
    date = models.DateField(auto_now=True)
    reply=models.CharField(max_length=200,null=True,blank=True)

#
#
# # view rating
# class View_Rating(models.Model):
#     User_name = models.TextField()
#     description=models.TextField()
#
# # Change Password
# class Change_Password(models.Model):
#     user = models.ForeignKey(Login, on_delete=models.CASCADE)
#     Current_Password=models.TextField()
#     New_Password=models.TextField()
#     Confirm_password = models.TextField()

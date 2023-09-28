from django import forms

from app1.models import Services, Login
from app1.models import Worker,Customer,Worker_schedule,Appointment,Complaint
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# THIS IS A SERVICE FORM USED BY THE ADMIN TO REPRESENT SERVICES

class ServiceForm(forms.ModelForm):
    class Meta:
        model=Services
        fields=('name',)



# THIS FORM IS A WORKER  FORM USED TO  GIVE THE WORKER DETAILS

class WorkerForm(forms.ModelForm):
     class Meta:
        model = Worker
        fields = ('name','address','phone_number','location','image')



class TimeInput(forms.TimeInput):
    input_type ='Time'

class DateInput(forms.DateInput):
    input_type='Date'

# THIS FORM IS USED TO  REPRESENT THE WORKER SCHEDULE

class Worker_scheduleForm(forms.ModelForm):
    date=forms.DateField(widget=DateInput)
    start_time=forms.TimeField(widget=TimeInput,)
    end_time = forms.TimeField(widget=TimeInput, )

    class Meta:
        model = Worker_schedule
        fields = ('start_time','end_time','date')




# THIS FORM IS LOGIN FORM USED FOR LOGIN PAGES

class LoginForm(UserCreationForm):
    class Meta:
        model = Login
        fields = ('username','password1','password2')





# THIS FORM IS A CUSTOMER  FORM USED TO  GIVE THE CUSTOMER DETAILS

class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=('name','address','phone_number','location')





# THIS FORM IS APPOINTMENT FORM USED BY WORKER TO TAKE APPOINTMENT OF CUSTOMER

class AppointmentForm(forms.ModelForm):
    class Meta:
        model =Appointment
        fields ='__all__'
        exclude =("status","user",'user1')





#### FORM IS  USED FOR COMPAAINTING AND SEND REPLY

class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ("description",)




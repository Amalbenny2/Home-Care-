from django import forms

from app1.models import Services, Login
from app1.models import Worker,Customer,Worker_schedule,Appointment,Complaint
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ServiceForm(forms.ModelForm):
    class Meta:
        model=Services
        fields=('name',)
class WorkerForm(forms.ModelForm):
     class Meta:
        model = Worker
        fields = ('name','address','phone_number','location','image')



class TimeInput(forms.TimeInput):
    input_type ='Time'

class DateInput(forms.DateInput):
    input_type='Date'
class Worker_scheduleForm(forms.ModelForm):
    date=forms.DateField(widget=DateInput)
    start_time=forms.TimeField(widget=TimeInput,)
    end_time = forms.TimeField(widget=TimeInput, )

    class Meta:
        model = Worker_schedule
        fields = ('start_time','end_time','date')



class LoginForm(UserCreationForm):
    class Meta:
        model = Login
        fields = ('username','password1','password2')


class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=('name','address','phone_number','location')



class AppointmentForm(forms.ModelForm):
    class Meta:
        model =Appointment
        fields ='__all__'
        exclude =("status","user",'user1')


class DateInput(forms.DateInput):
    input_type='Date'
class ComplaintForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    class Meta:
        model = Complaint
        fields = '__all__'








from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from .forms import ServiceForm, WorkerForm, LoginForm, CustomerForm, Worker_scheduleForm,AppointmentForm,ComplaintForm
from .models import Services, Worker, Customer, Worker_schedule, Login,Appointment,Complaint


#################################ADMIN DASHBOARD########################
def home(request):
    return render(request, 'admintemp/Homepage.html')

def admin_home(request):
    return render(request, 'admintemp/index.html')


def add_services(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'admintemp/Services.html', {'form': form})


def service_view(request):
    obj = Services.objects.all()
    return render(request, 'admintemp/service_view.html', {'obj': obj})


def service_delete(request, id):
    form = Services.objects.get(id=id)
    form.delete()
    return redirect("service_view")


def worker_register(request):
    worker_form = WorkerForm()
    login_form = LoginForm()
    if request.method == 'POST':
        worker_form = WorkerForm(request.POST, request.FILES)
        login_form = LoginForm(request.POST)
        if worker_form.is_valid() and login_form.is_valid():  # checking whether values given to the form is valid
            user = login_form.save(commit=False)
            user.is_Worker = True
            user.save()
            worker = worker_form.save(commit=False)
            worker.user = user
            worker.save()
            return redirect('login_view')
    return render(request, 'admintemp/Worker_register.html', {'worker_form': worker_form, 'login_form': login_form})


def Worker_view(request):
    obj = Worker.objects.all()
    return render(request, 'admintemp/Worker_view.html', {'obj': obj})


def Worker_edit_views(request, id):
    obj = Worker.objects.get(id=id)
    form = WorkerForm(instance=obj)
    if request.method == 'POST':
        form = WorkerForm(request.POST or None, instance=obj)
        form.save()
    return render(request, 'admintemp/Worker_edit_views.html', {'form': form})


def Worker_delete_views(request, id):
    form = Worker.objects.get(id=id)
    form.delete()
    return redirect("Worker_view")


def Customer_view(request):
    obj = Customer.objects.all()
    return render(request, 'admintemp/Customer_view.html', {'obj': obj})


def Customer_edit_views(request, id):
    obj = Customer.objects.get(id=id)
    form = CustomerForm(instance=obj)
    if request.method == 'POST':
        form = CustomerForm(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()

    return render(request, 'admintemp/Customer_edit_view.html', {'form': form})


def Customer_delete_views(request, id):
    form = Customer.objects.get(id=id)
    form.delete()
    return redirect("Customer_view")


##############################################ADMIN DASHBOARD ENDS##########

def Profile(request):
    u=request.user
    obj=Login.objects.get(username=u)
    data=Worker.objects.filter(user=obj)
    print(data)
    return render(request,'Workertemp/Worker_profile_view.html',{'data':data})

def Worker_home(request):
    return render(request, 'Workertemp/Worker_home.html')

def Schedule_add(request):
    form = Worker_scheduleForm()
    if request.method == 'POST':
        form = Worker_scheduleForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.user=Worker.objects.get(user=request.user)
            form.save()
            return redirect('Worker_home')
    return render(request, 'Workertemp/schedule_add.html', {'form': form})


def Worker_schedule_view(request):
    data = Worker.objects.get(user=request.user)
    obj = Worker_schedule.objects.filter(user=data)
    return render(request, 'Workertemp/Worker_schedule_view.html', {'obj': obj})


def Worker_schedule_edit(request, id):
    obj = Worker_schedule.objects.get(id=id)
    form = Worker_scheduleForm(instance=obj)
    if request.method == 'POST':
        form = Worker_scheduleForm(request.POST or None, instance=obj)
        form.save()
    return render(request, "Workertemp/Worker_schedule_edit.html", {'form': form})



def Worker_schedule_delete(request, id):
    form = Worker_schedule.objects.get(id=id)
    form.delete()
    return redirect('Worker_schedule_view')


def register(request):
    form = LoginForm
    return render(request, "register.html", {"form": form})


# Worker view starts


# Customer view starts


def Customer_register(request):
    customer_form = CustomerForm()
    login_form = LoginForm()
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, request.FILES)
        login_form = LoginForm(request.POST)
        if customer_form.is_valid() and login_form.is_valid():
            user = login_form.save(commit=False)
            user.is_Customer = True
            user.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('login_view')
    return render(request, 'Customertemp/Customer_register.html', {'customer_form': customer_form, 'login_form': login_form})





def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_home')
            elif user.is_Worker:
                return redirect('Worker_home')
            elif user.is_Customer:
                return redirect('Customer_home')
            else:
                messages.info(request, "INVALID CREDENTIALS")
    return render(request, 'login.html')

def Customer_home(request):
    return render(request,'customertemp/Customer_home.html')


###########################Worker Dashboard############################################




def Customer_profile(request):
    u=request.user
    obj=Login.objects.get(username=u)
    data=Customer.objects.filter(user=obj)
    print(data)
    return render(request,'customertemp/Customer_profile.html',{'data':data})


def Customer_schedule_view(request):
    # data = Worker.objects.get(user=request.user)
    obj = Worker_schedule.objects.all()
    return render(request, 'Customertemp/Customer_schedule_view.html', {'obj': obj})



# def Appointment_views(request):
#     i = Worker.objects.filter.get(user=request.user)
#     appointment = Appointment.objects.filter(Worker=i)
#     return render(request, 'Workertemp/view_appointment.html', {'appointment': appointment})
def Appointment_views(request):
    appointment = Appointment.objects.all()
    return render(request, 'Workertemp/view_appointment.html', {'appointment': appointment})
# def view_appointment_user(request):
#     u = Customer.objects.get(user=request.user)
#     appointment = Appointment.objects.filter(user=u)
#     return render(request, 'Customertemp/view_appointment_user.html', {'appointments': appointment})
def approve_appointment(request, id):
        appointment = Appointment.objects.get(id=id)
        appointment.status = 1
        appointment.save()
        return redirect('Appointment_views')

def reject_appointment(request, id):
        appointment = Appointment.objects.get(id=id)
        if request.method == 'POST':
            appointment.status = 2
            appointment.save()
            return redirect('Appointment_views')
        return render(request, 'Workertemp/reject_appointment.html')

def take_appointment(request,id):
    schedule = Worker_schedule.objects.get(id=id)
    print(schedule)
    u = Customer.objects.get(user=request.user)
    print(u)
    appointment = Appointment.objects.filter(user=u,Worker_schedule=schedule)
    print(appointment)
    if appointment.exists():
        messages.info(request,'you have already requested for this schedule')
        return redirect('Customer_schedule_view')
    else:
        if request.method == 'POST':
            obj = Appointment()
            obj.user = u
            obj.Worker_schedule = schedule
            obj.save()
            messages.info(request,'Appointment Booked Successfully')
            return redirect('view_appointment_user')
    return render(request, 'customertemp/take_appointment.html', {'schedule': schedule})


def view_appointment_user(request):
    u = Customer.objects.get(user=request.user)
    appointment = Appointment.objects.filter(user=u)
    return render(request, 'Customertemp/view_appointment_user.html', {'appointment': appointment})




def Complaint(request):
    u = Customer.objects.get(user=request.user)
    form=ComplaintForm()

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request,'Customertemp/Complaint.html',{'form':form})


def complaint_view(request):
    obj=Complaint.objects.all()
    return render(request,'Customertemp/omplaint_view.html',{'obj':obj})



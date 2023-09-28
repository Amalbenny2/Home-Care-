from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template import loader

from app1.forms import ServiceForm, WorkerForm, LoginForm, CustomerForm, Worker_scheduleForm,AppointmentForm,ComplaintForm
from app1 .models import Services, Worker, Customer, Worker_schedule, Login,Appointment,Complaint


#################################ADMIN DASHBOARD########################
def home(request):
    return render(request, 'admintemp/Homepage.html')



# HERE THE VIEWS DEFINES LOGIN VIEW (ADMIN HOMEPAGE)
@login_required(login_url='login_view')
def admin_home(request):
    return render(request, 'admintemp/index.html')



# HERE THE VIEWS DEFINES LOGIN VIEW OF USER IF STAFF/WORKER/CUSTOMER WHILE LOGIN IN AND REDIRECTING TO THERE OWN HOMEPAGE
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





# HERE THE VIEWS DEFINES WHAT SERVICES THAT ARE  ADDED BY ADMIN
@login_required(login_url='login_view')
def add_services(request):
    form = ServiceForm()
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'admintemp/Services.html', {'form': form})



# HERE THE VIEWS DEFINES WHAT SERVICES ARE PROVIDED BY THE ADMIN TO THE USERS/CUSTOMERS
@login_required(login_url='login_view')
def service_view(request):
    obj = Services.objects.all()
    return render(request, 'admintemp/service_view.html', {'obj': obj})



# HERE THE VIEWS DEFINES WHAT SREVICES ARE GET DELETED
@login_required(login_url='login_view')
def service_delete(request, id):
    form = Services.objects.get(id=id)
    form.delete()
    return redirect("service_view")




# HERE THE VIEWS DEFINES THE REGISTRATION OF NEW WORKER
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





# THIS VIEW DEFINES THE REGISTRATION FORMS
def register(request):
    form = LoginForm
    return render(request, "register.html", {"form": form})



# HERE THE  ADMIN CAN VIEW WHICH WORKERS ARE REGISTERED
@login_required(login_url='login_view')
def Worker_view(request):
    obj = Worker.objects.all()
    return render(request, 'admintemp/Worker_view.html', {'obj': obj})



# HERE THE VIEWS  OF WORKER CAN BE  EDITED BY ADMIN
@login_required(login_url='login_view')
def Worker_edit_views(request, id):
    obj = Worker.objects.get(id=id)
    form = WorkerForm(instance=obj)
    if request.method == 'POST':
        form = WorkerForm(request.POST or None, instance=obj)
        form.save()
    return render(request, 'admintemp/Worker_edit_views.html', {'form': form})



# HERE THE VIEWS DEFINES  WORKER IS  DELETED BY ADMIN
@login_required(login_url='login_view')
def Worker_delete_views(request, id):
    form = Worker.objects.get(id=id)
    form.delete()
    return redirect("Worker_view")




# HERE THE  ADMIN CAN VIEW  THE CUSTOMERS WHO GET REGISTERED
@login_required(login_url='login_view')
def Customer_view(request):
    obj = Customer.objects.all()
    return render(request, 'admintemp/Customer_view.html', {'obj': obj})



# HERE VIEWS CAN EDIT THE CUSTOMER FORMS
@login_required(login_url='login_view')
def Customer_edit_views(request, id):
    obj = Customer.objects.get(id=id)
    form = CustomerForm(instance=obj)
    if request.method == 'POST':
        form = CustomerForm(request.POST or None, instance=obj)
        if form.is_valid():
            form.save()

    return render(request, 'admintemp/Customer_edit_view.html', {'form': form})




# HERE THE  VIEWS CAN DELETE  CUSTOMER FORM
@login_required(login_url='login_view')
def Customer_delete_views(request, id):
    form = Customer.objects.get(id=id)
    form.delete()
    return redirect("Customer_view")



# HERE  THE ADMIN CAN VIEW THE COMPLAINT THAT GIVEN BY THE CUSTOMER
@login_required(login_url='login_view')
def Complaint_view(request):
    obj=Complaint.objects.all()
    return render(request,'admintemp/Complaint_view.html',{'obj':obj})



# HERE THE ADMIN CAN GIVE REPLY  TO CUSTOMERS COMPLAINT
@login_required(login_url='login_view')
def reply(request, id):
    complaint = Complaint.objects.get(id=id)
    if request.method == "POST":
      r=request.POST.get('reply')
      complaint.reply = r
      complaint.save()
      messages.info(request,'Reply send form Complaint')
      return redirect('Complaint_view')
    return render(request,'admintemp/reply.html',{'complaint':complaint})



############################################## WORKER DASHBOARD ############################################


# HERE WORKER WHO LOGIN CAN VIEW THERE PROFILE
@login_required(login_url='login_view')
def Profile(request):
    u=request.user
    obj=Login.objects.get(username=u)
    data=Worker.objects.filter(user=obj)
    print(data)
    return render(request,'Workertemp/Worker_profile_view.html',{'data':data})




# THIS IS THE WORKERS HOME PAGE (WORKER REACH AFTER THEY GET LOGGIED IN)
@login_required(login_url='login_view')
def Worker_home(request):
    return render(request, 'Workertemp/Worker_home.html')



# THIS VIEW ADD THE SCHEDULE OF THE WORKER WHEN THEY ARE AVAILABLE R WORK
@login_required(login_url='login_view')
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



# HERE WORKER CAN VIEW THE TIME SCHEDULE BY HIM SELF
@login_required(login_url='login_view')
def Worker_schedule_view(request):
    data = Worker.objects.get(user=request.user)
    obj = Worker_schedule.objects.filter(user=data)
    return render(request, 'Workertemp/Worker_schedule_view.html', {'obj': obj})



# HERE THE WORKER CAN EDIT THER SCHEDULE
@login_required(login_url='login_view')
def Worker_schedule_edit(request, id):
    obj = Worker_schedule.objects.get(id=id)
    form = Worker_scheduleForm(instance=obj)
    if request.method == 'POST':
        form = Worker_scheduleForm(request.POST or None, instance=obj)
        form.save()
    return render(request, "Workertemp/Worker_schedule_edit.html", {'form': form})



# HERE THE WORKER CAN  DELETE THERE  SCHEDULE
@login_required(login_url='login_view')
def Worker_schedule_delete(request, id):
    form = Worker_schedule.objects.get(id=id)
    form.delete()
    return redirect('Worker_schedule_view')


# IN THIS VIEWS WORKER CAN VIEW THE CUSTOMER WHO WANTS TO TAKE APPOINTMENT OF THE WORKER AND WHETHER HE CAN ACCEPTS OR REJECTS IT
@login_required(login_url='login_view')
def Appointment_views(request):
    appointment = Appointment.objects.all()
    return render(request, 'Workertemp/view_appointment.html', {'appointment': appointment})



# HERE THE WORKER APPROVES THE APPOINTMENT OF CUSTOMER
@login_required(login_url='login_view')
def approve_appointment(request, id):
        appointment = Appointment.objects.get(id=id)
        appointment.status = 1
        appointment.save()
        return redirect('Appointment_views')




# HERE THE WORKER CAN REJECT THE APPOINTMET REQUEST THAT SEND BY THE CUSTOMER
@login_required(login_url='login_view')
def reject_appointment(request, id):
        appointment = Appointment.objects.get(id=id)
        if request.method == 'POST':
            appointment.status = 2
            appointment.save()
            return redirect('Appointment_views')
        return render(request, 'Workertemp/reject_appointment.html')










########################### Customer Dashboard ############################################



# HERE CUSTOMER CAN GET REGISTER TO THIS
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



# HERE CUSTOMER CAN VIEW THER PROFILE AFTER REGISTRATION AND LOGIN TO THERE OWN HOME PAGE
@login_required(login_url='login_view')
def Customer_profile(request):
    u=request.user
    obj=Login.objects.get(username=u)
    data=Customer.objects.filter(user=obj)
    print(data)
    return render(request,'customertemp/Customer_profile.html',{'data':data})




# HERE THE CUSTOMER HOME PAGE (WHERE THE CUSTOMER GETS AFTER LOGIN)
@login_required(login_url='login_view')
def Customer_home(request):
    return render(request,'customertemp/Customer_home.html')




# HERE THE CUSTOMER CAN VIEW THE  THE SCHEDULE ADDED BY THE WORKER
@login_required(login_url='login_view')
def Customer_schedule_view(request):
    obj = Worker_schedule.objects.all()
    return render(request, 'Customertemp/Customer_schedule_view.html', {'obj': obj})







# HERE THE CUSTOMER CAN REQUEST APPOINTMENT OF WORKER
@login_required(login_url='login_view')
def take_appointment(request,id):
    schedule = Worker_schedule.objects.get(id=id)
    u = Customer.objects.get(user=request.user)
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




# HERE THE CUSTOMER CAN  VIEW  WHOM THERE ARE  APPLY REQUEST FOR WORK
@login_required(login_url='login_view')
def view_appointment_user(request):
    u = Customer.objects.get(user=request.user)
    appointment = Appointment.objects.filter(user=u)
    return render(request, 'Customertemp/view_appointment_user.html', {'appointment': appointment})



# HERE THE CUSTOMER CAN GIVE THE COMPLAINT  TO THE ADMIN
@login_required(login_url='login_view')
def Complaint_send(request):
    form=ComplaintForm()
    user=request.user

    if request.method == 'POST':
         form=ComplaintForm(request.POST)
         if form.is_valid():
             obj=form.save(commit=False)
             obj.user = user
             obj.save()
    return render(request,'Customertemp/Complaint.html',{'form':form})




# HERE THE COMPLAINT CAN BE GET DELETED
@login_required(login_url='login_view')
def Complaint_delete(request,id):
    complaint = Complaint.objects.get(id=id)
    complaint.delete()
    return redirect('Complaint_view')



# HERE THE WORKER SCHEDULE CAN GET DELETED IN THIS VIEW
@login_required(login_url='login_view')
def Worker_schedule_delete(request, id):
    form = Worker_schedule.objects.get(id=id)
    form.delete()
    return redirect('Worker_schedule_view')




# HERE THE CUSTOMER CAN VIEW THE REPLY GIVEN BY ADMIN FOR THE COMPLAINT
@login_required(login_url='login_view')
def reply_view(request):
    complaint = Complaint.objects.all()
    return render(request,'customertemp/reply_view.html',{'complaint':complaint})



# HERE WE CAN LOGOUT FORM PAGES
def logout_view(request):
    logout(request)
    return redirect('login_view')


   




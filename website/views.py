from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignupForm,AddRecordForm
from .models import Record,Communication
from .forms import CommunicationForm
from django.core.mail import send_mail
from django.http import JsonResponse

def home(request):
    records=Record.objects.all()
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']

        #Authentication
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'You have been Logged In')
            return redirect('home')
        else:
            messages.error(request,'Try again later...')
            return redirect('home')
    else:
        return render(request,'home.html',{'records':records})

def logout_user(request):
    logout(request)
    messages.success(request,'Logged Out Successfully')
    return redirect('home')


def register_user(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,'Registered Successfully!')
            return redirect('home')
    else:
        form=SignupForm()
        return render(request,'register.html',{'form':form})
    return render(request,'register.html',{'form':form}) 


def customer_record(request,pk):
    customer_record = get_object_or_404(Record, id=pk)
    return render(request, 'record.html', {'customer_record': customer_record})
 
def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it=Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request,'Deleted Successfully!')
        return redirect('home')
    else:
        messages.success(request,'You Must be Logged in to delete the record!')
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST)
    if request.method == 'POST':
        
        if request.user.is_authenticated:  
            if form.is_valid():
                add_record = form.save()
                messages.success(request, 'Added Successfully')
                return redirect('home')
        else:
            messages.error(request, 'You must be logged in to add a record')
            return redirect('home')
        
    return render(request, 'add_record.html', {'form': form})           

def update_record(request,pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form=AddRecordForm(request.POST or None,instance= current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to update a record')
        return redirect('home')



def contact_screen(request, customer_id):
    customer = get_object_or_404(Record, id=customer_id)
    communications = Communication.objects.filter(customer=customer)
    form = CommunicationForm(request.POST or None)
    if form.is_valid():
        communication = form.save(commit=False)
        communication.customer = customer
        communication.save()
        # Optionally, send email here
        send_mail(
            'New communication added',
            communication.conversation,
            'chebolusaiteja@email.com',  # Sender's email
            [customer.email],  # Recipient's email
            fail_silently=False,
        )
        return redirect('contact_screen', customer_id=customer_id)
    return render(request, 'contact_screen.html', {'customer': customer, 'communications': communications, 'form': form})

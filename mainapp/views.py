from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import requests
# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if(request.method == 'POST'):
        name= request.POST.get('name')
        contactno= request.POST.get('contactno')
        email= request.POST.get('email')
        subject= request.POST.get('subject')
        message= request.POST.get('message')
        enq= Enquiry(name=name, contactno=contactno, email=email, subject=subject , message=message)
        enq.save()
        url = "http://sms.bulkssms.com/submitsms.jsp"
        params = {
            "user": "BRIJESH",
            "key": "066c862acdXX",
            "mobile": f"{contactno}",
            "message": "Thanks for enquiry we will contact you soon.\n\n-Bulk SMS",
            "senderid": "UPDSMS",
            "accusage": "1",
            "entityid": "1201159543060917386",
            "tempid": "1207169476099469445"
        }
        response = requests.get(url, params=params)
        print("Response:", response.text)
        messages.success(request , "Form submition successfull")
        return redirect('contact')
    return render(request, 'contact.html')

def signin(request):
    if request.method =='POST':
        usertype = request.POST.get('usertype')
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            log = LoginInfo.objects.get(username=username,password=password ,usertype=usertype)
            if log is not None:
                if log.usertype=="homeowner":
                    request.session['homeownerid']= username
                    messages.success(request,'Welcome Homeowner')
                    return redirect('homeownerdash')
                elif log.usertype== "contractor":
                    request.session['contractorid']= username
                    messages.success(request,'Welcome Contractor')
                    return redirect('contractordash')
                else:
                    messages.error(request,'Invalid information')
                    return redirect('signin')
        except LoginInfo.DoesNotExist:
            messages.error(request,'Invalid username or password')
            return redirect('signin')
    return render(request, 'signin.html')

def register(request):
    if request.method == 'POST':
        usertype= request.POST.get('usertype')
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        password = request.POST.get('password')
        u= LoginInfo.objects.filter(username=email)
        if u:
            messages.error(request,"Email already exist")
            return redirect('register')
        
        log = LoginInfo(usertype=usertype,username=email,password=password)
        user = UserInfo(name=name,email=email,contactno=contactno,password=password,usertype=usertype,login=log)
        log.save()
        user.save()
        messages.success(request,"Thank you for join us")
        return redirect('signin')
    return render(request, 'register.html')

def project(request):
    return render(request, 'project.html')

def service(request):
    return render(request, 'service.html')

def self(request):
    return render(request, 'self.html')

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usertype='admin'
        try:
            ad= LoginInfo.objects.get( usertype=usertype  ,username = username , password = password)
            if ad is not None:
                request.session['adminid']= username #for session
                messages.success(request, "Welcome Admin")
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request, "Your username or password is wrong")
            return redirect('adminlogin')
    return render(request, 'adminlogin.html')



def forget(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        try:
            user = UserInfo.objects.get(email=email, contactno=contactno)
        
            if user is not None:
                url = "http://sms.bulkssms.com/submitsms.jsp"
                params = {
                    "user": "BRIJESH",
                    "key": "066c862acdXX",
                    "mobile": f"{user.contactno}",
                    "message": f"Your Password is {user.password}\n\n-Bulk SMS",
                    "senderid": "UPDSMS",
                    "accusage": "1",
                    "entityid": "1201159543060917386",
                    "tempid": "1207169476099469445"
                }
                response = requests.get(url, params=params)
                print("Response:", response.text)
                messages.success(request, "Your password has been sent to your registered mobile number.")
                return redirect('signin')
            else:
                messages.error(request, "Invalid username or contact number.")
                return redirect('forget')
        except UserInfo.DoesNotExist:
            messages.error(request, "Accept block.")
            return redirect('forget')
    return render(request, 'forget.html')


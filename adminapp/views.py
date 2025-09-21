from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from homeownerapp.models import *
from django.views.decorators.cache import cache_control


# Create your views here.
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context={
        'adminid':adminid,
        'th':UserInfo.objects.filter(login__usertype='homeowner').count(),
        'tc':UserInfo.objects.filter(login__usertype='contractor').count(),
        'tu':UserInfo.objects.all().count(),
        'pr':Project.objects.all().count(),
        'pp':Enquiry.objects.all().count(),
        'pc':Project.objects.filter(status='completed').count(),
        'po':Project.objects.filter(status='under_construction').count(),
        'op':Project.objects.filter(status='under_construction'),
    }
    return render(request, 'admindash.html',context)
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request,"You are logged out")
        return redirect('adminlogin')
    else:
        return redirect('index')
    


#view for enquiry
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def viewenq(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('adminlogin')
    enqs= Enquiry.objects.all()
    adminid=request.session.get('adminid')
    return render(request, 'viewenq.html' , { 'enqs':enqs,'adminid':adminid })


#deletion process for enquiry
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def delenq(request,id):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('adminlogin')
    enq= Enquiry.objects.get(id=id)
    enq.delete()
    messages.success(request,'Enquiry delected successfully')
    return redirect('viewenq')

@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def adminchangepass(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('adminchangepass')
    adminid=request.session.get('adminid')
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try:
            admin = LoginInfo.objects.get(username=adminid)
            if admin.password != oldpwd :
                messages.error(request,'Old password is worng')
                return redirect('adminchangepass')
            elif newpwd != confirmpwd:
                messages.error(request,'New paasword and confirm password are not match')
                return redirect('adminchangepass')
            elif admin.password == newpwd:
                messages.error(request,'new password is same as old password')
                return redirect('adminchangepass')
            else:
                admin.password = newpwd
                admin.save()
                messages.success(request, 'Password changed successfully')
                return redirect('admindash')

        except LoginInfo.DoesNotExist:
            messages.error(request,"Somethings went wrong")
            return redirect('adminlogin')
    return render(request,'adminchangepass.html',{'adminid':adminid})

@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def managecontractors(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    contractor = UserInfo.objects.filter(usertype='contractor')
    user=LoginInfo.objects.filter(usertype='contractor')
    return render(request,'managecontractors.html' ,{'adminid':adminid,'contractor':contractor,'user':user})



@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def managehomeowners(request):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    homeowner= UserInfo.objects.filter(usertype='homeowner')
    user=LoginInfo.objects.filter(usertype='homeowner')
    return render(request,'managehomeowners.html' ,{'adminid':adminid,'homeowner':homeowner,'user':user})

def block(request,id):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    user=LoginInfo.objects.get(username=id)
    user.status='blocked'
    user.save()
    if user.usertype=='homeowner':
        return redirect('managehomeowners')
    elif user.usertype=='contractor':
        return redirect('managecontractors')
    
def unblock(request,id):
    if not 'adminid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    user=LoginInfo.objects.get(username=id)
    user.status='active'
    user.save()
    if user.usertype=='homeowner':
        return redirect('managehomeowners')
    elif user.usertype=='contractor':
        return redirect('managecontractors')


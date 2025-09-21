from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from .forms import ProjectForm
from homeownerapp.models import *
from contractorapp.models import *
from django.utils import timezone
from django.views.decorators.cache import cache_control

# Create your views here.

@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def homeownerdash(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('signin')
    homeownerid=request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
            'name': homeowner.name,
            'homeownerid': homeownerid,
            'homeowner':homeowner,
            'tp':Project.objects.filter(homeowner=homeowner).count(),
            'op':Project.objects.filter(homeowner=homeowner,status='under_construction').count(),
            'cp':Project.objects.filter(homeowner=homeowner,status='completed').count(),
            'pp':Project.objects.filter(homeowner=homeowner,status='planned').count(),

    }
    return render(request, 'homeownerdash.html',context)



@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def homeLogout(request):
    if 'homeownerid' in request.session:
        del request.session['homeownerid']
        messages.success(request,"You are logged out ccessfully")
        return redirect('signin')
    else:
        return redirect('index')
    


@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def hchangepass(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('signin')
    homeownerid=request.session.get('homeownerid')
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try:
            login = LoginInfo.objects.get(username=homeownerid)
            home = UserInfo.objects.get(email=homeownerid)
            if home.password != oldpwd :
                messages.error(request,'Old password is incorrect')
                return redirect('hchangepass')
            elif newpwd != confirmpwd:
                messages.error(request,'New paasword and confirm password are not match')
                return redirect('hchangepass')
            elif home.password == newpwd:
                messages.error(request,'new password is same as old password')
                return redirect('hchangepass')
            else:
                home.password = newpwd
                login.password=newpwd
                login.save()
                home.save()
                messages.success(request, 'Password changed successfully')
                return redirect('homeownerdash')
        except UserInfo.DoesNotExist:
            messages.error(request,"Somethings went wrong")
            return redirect('signin')
            
    homeownerid=request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
            'name': homeowner.name,
            'homeownerid': homeownerid,
            'homeowner':homeowner,
    }
    return render(request,'hchangepass.html',context)



@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def homeownerprofile(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('signin')
    homeownerid=request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
            'name': homeowner.name,
            'homeownerid': homeownerid,
            'homeowner':homeowner,

    }
    return render(request, 'homeownerprofile.html',context)


@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def homeowneredit(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('signin')
    homeownerid=request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    context = {
            'name': homeowner.name,
            'homeownerid': homeownerid,
            'homeowner':homeowner,

    }
    if request.method == "POST":
        name=request.POST.get('name')
        contactno=request.POST.get('contactno')
        address=request.POST.get('address')
        bio=request.POST.get('bio')
        profile=request.FILES.get('profile')
        homeowner.name=name
        homeowner.contactno=contactno
        homeowner.address=address
        homeowner.bio=bio
        if profile:
            homeowner.picture=profile
        homeowner.save()
        messages.success(request,"Your Profile has been uploaded")
        return redirect('homeownerprofile')
    return render(request, 'homeowneredit.html',context)



@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def addproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('signin')
    homeownerid=request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    form= ProjectForm()
    context = {
            'name': homeowner.name,
            'homeownerid': homeownerid,
            'homeowner':homeowner,
            'form':form,

    }
    if request.method =='POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.homeowner= homeowner
            project.save()
            messages.success(request,"Project has been added")
            return redirect('addproject')
        else:
            messages.error(request,"Invalid form")
            return redirect('addproject')
    return render(request,'addproject.html',context)


@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def hviewproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('signin')
    homeownerid=request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner)
    context = {
            'name': homeowner.name,
            'homeownerid': homeownerid,
            'homeowner':homeowner,
            'projects':projects,

    }
    return render(request, 'hviewproject.html',context)



@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def hrunproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('signin')
    homeownerid=request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects = Project.objects.filter(homeowner=homeowner , status='under_construction')
    context = {
            'name': homeowner.name,
            'homeownerid': homeownerid,
            'homeowner':homeowner,
            'projects':projects,

    }
    return render(request, 'hrunproject.html',context)





@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def hcompleteproject(request):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('signin')
    homeownerid=request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    projects=Project.objects.filter(homeowner=homeowner,status='completed')
    context = {
            'name': homeowner.name,
            'homeownerid': homeownerid,
            'homeowner':homeowner,
            'projects':projects,

    }
    return render(request, 'hcompleteproject.html',context)




@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def hviewapplications(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    project=Project.objects.get(id=id)
    applications=ContractorApplication.objects.filter(project=project)
    context={
        'name': homeowner.name,
        'homeownerid': homeownerid,
        'homeowner':homeowner,
        'project':project,
        'applications':applications
    }
    return render(request,'hviewapplications.html',context)


@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def rejectapp(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    app= ContractorApplication.objects.get(id=id)
    app.status = 'rejected'
    app.save()
    messages.success(request,"Application has been rejected")
    return redirect('hviewapplications', id=app.project.id)




@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def approveapp(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    homeownerid=request.session.get('homeownerid')
    homeowner=UserInfo.objects.filter(email=homeownerid).first()
    app= ContractorApplication.objects.get(id=id)
    project = Project.objects.get(id=app.project.id)
    apps= ContractorApplication.objects.filter(project=app.project).update(status='rejected')
    app.status = 'approved'
    app.save()
    project.contractor = app.contractor
    project.start_date = timezone.now()
    project.status = 'under_construction'
    project.save()
    messages.success(request,"Application has been approved")
    return redirect('hviewapplications', id=app.project.id)




@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def viewupdates(request,id):
    if not 'homeownerid' in request.session:
        messages.error(request,'You are not logged in')
        return redirect('signin')
    homeownerid=request.session.get('homeownerid')
    homeowner = UserInfo.objects.filter(email=homeownerid).first()
    project = Project.objects.get(id=id)
    updates = ProgressUpdate.objects.filter(project=project)
    context = {
            'name': homeowner.name,
            'homeownerid': homeownerid,
            'homeowner':homeowner,
            'project':project,
            'updates':updates,

    }
    return render(request, 'viewupdates.html',context)
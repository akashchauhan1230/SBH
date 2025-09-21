from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from homeownerapp.models import *
from .models import *
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def contractordash(request):
    if 'contractorid' not in request.session:
        messages.error(request, 'You are not logged in')
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
  
    context = {
        'name': contractor.name ,
        'contractorid': contractorid,
        'contractor':contractor,
        'tp':Project.objects.filter(contractor=contractor).count(),
            'op':Project.objects.filter(contractor=contractor,status='under_construction').count(),
            'cp':Project.objects.filter(contractor=contractor,status='completed').count(),
            'pp':Project.objects.filter(contractor=contractor,status='planned').count(),
            'co':Project.objects.filter(contractor=contractor,status='under_construction'),
           
    }
    return render(request, 'contractordash.html', context)


@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def conLogout(request):
    if 'contractorid' in request.session:
        del request.session['contractorid']
        messages.success(request,"You are logged out")
        return redirect('signin')
    else:
        return redirect('index')
    



@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def conchangepass(request):
    if 'contractorid' not in request.session:
        messages.error(request, 'You are not logged in')
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try:
            login = LoginInfo.objects.get(username=contractorid)
            con = UserInfo.objects.get(email=contractorid)
            if con.password != oldpwd:
                messages.error(request, 'Old password is wrong')
                return redirect('conchangepass')
            elif newpwd != confirmpwd:
                messages.error(request, 'New password and confirm password do not match')
                return redirect('conchangepass')
            elif con.password == newpwd:
                messages.error(request, 'New password is same as old password')
                return redirect('conchangepass')
            else:
                con.password = newpwd
                login.password = newpwd
                login.save()
                con.save()
                messages.success(request, 'Password changed successfully')
                return redirect('contractordash')
        except UserInfo.DoesNotExist:
            messages.error(request, "Something went wrong")
            return redirect('signin')

    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    context = {
        'name': contractor.name,
        'contractorid': contractorid,
        'contractor':contractor,
    }
    return render(request, 'conchangepass.html', context)




@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def conprofile(request):
    if 'contractorid' not in request.session:
        messages.error(request, 'You are not logged in')
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    context = {
        'name': contractor.name,
        'contractorid': contractorid,
        'contractor':contractor,
    }
    return render(request, 'conprofile.html', context)



@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def coneditprofile(request):
    if 'contractorid' not in request.session:
        messages.error(request, 'You are not logged in')
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    context = {
        'name': contractor.name,
        'contractorid': contractorid,
        'contractor':contractor,
    }
    if request.method == "POST":
        name=request.POST.get('name')
        contactno=request.POST.get('contactno')
        address=request.POST.get('address')
        bio=request.POST.get('bio')
        profile=request.FILES.get('profile')
        contractor.name=name
        contractor.contactno=contactno
        contractor.address=address
        contractor.bio=bio
        if profile:
            contractor.picture=profile
        contractor.save()
        messages.success(request,"Your Profile has been uploaded")
        return redirect('conprofile')
    return render(request, 'coneditprofile.html', context)



@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def cviewprojects(request):
    if 'contractorid' not in request.session:
        messages.error(request, 'You are not logged in')
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    projects = Project.objects.filter(contractor=None)
    context = {
        'name': contractor.name ,
        'contractorid': contractorid,
        'contractor':contractor,
        'projects':projects,
    }
    return render(request, 'cviewprojects.html', context)




@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def applyproject(request,id):
    if 'contractorid' not in request.session:
        messages.error(request, 'You are not logged in')
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    project = Project.objects.get(id=id)
    context = {
        'name': contractor.name ,
        'contractorid': contractorid,
        'contractor':contractor,
        'project':project,
    }
    application = ContractorApplication.objects.filter(project=project,contractor=contractor)
    if application.exists():
        messages.warning(request,"You have already applied for this project")
        return redirect('cviewprojects')
    if request.method =='POST':
        proposal_text = request.POST.get('proposal_text')
        design_file = request.FILES.get('design_file')
        estimated_budget = request.POST.get('estimated_budget')
        estimated_duration = request.POST.get('estimated_duration')
        app = ContractorApplication(contractor=contractor , project=project , proposal_text=proposal_text , design_file=design_file , estimated_budget=estimated_budget , estimated_duration=estimated_duration)
        app.save()
        messages.success(request,"Project application submitted successfully")
        return redirect('cviewprojects')
    return render(request, 'applyproject.html', context)



@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def capplications(request):
    if not 'contractorid' in request.session:
        messages.error(request,'You are not logged in ')
        return redirect('login')
    contractorid=request.session.get('contractorid')
    contractor=UserInfo.objects.filter(email=contractorid).first()
    applications=ContractorApplication.objects.filter(contractor=contractor)
    context={
        'name': contractor.name ,
        'contractorid': contractorid,
        'contractor':contractor,
        'applications':applications
    }
    return render(request,'capplications.html',context)




@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def assignedprojects(request):
    if 'contractorid' not in request.session:
        messages.error(request, 'You are not logged in')
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    projects = Project.objects.filter(contractor=contractor)
    context = {
        'name': contractor.name ,
        'contractorid': contractorid,
        'contractor':contractor,
        'projects':projects,
    }
    return render(request, 'assignedprojects.html', context)







@cache_control(no_cache=True ,must_revalidate=True ,no_store=True)
def addprogress(request,id):
    if 'contractorid' not in request.session:
        messages.error(request, 'You are not logged in')
        return redirect('signin')
    contractorid = request.session.get('contractorid')
    contractor = UserInfo.objects.filter(email=contractorid).first()
    project = Project.objects.get(id=id)
    context = {
        'name': contractor.name ,
        'contractorid': contractorid,
        'contractor':contractor,
        'project':project,
    }
    if request.method == 'POST':
        update_text= request.POST.get('update_text')
        progress_percent= int(request.POST.get('progress_percent'))
        image= request.FILES.get('image')
        pu=ProgressUpdate(project=project,update_text=update_text,progress_percent=progress_percent ,updated_by=contractor ,image=image)
        if progress_percent > 100:
            messages.error(request,"Progress cannot be more than 100%")
            return redirect('addprogress',id=id)
        elif progress_percent < 0 or progress_percent < project.progress :
            messages.error(request,"Progress cannot be less than 0% or current progress")
            return redirect('addprogress',id=id)
        if progress_percent == 100:
            project.status = 'completed'
        project.progress = progress_percent
        project.save()
        pu.save()
        messages.success(request,"Progress updates successfully")
        return redirect('addprogress',id=id)
    return render(request, 'addprogress.html', context)
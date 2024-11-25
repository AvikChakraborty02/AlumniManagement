from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from alumniapp.models import OTP,Coordinator,Application,Alumni,Posts,Events
from django.db.models import Q

import json
import os

import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator

# Create your views here.

#Common page 

def home(req):
    # Fetch 9 random alumni records
    alumni_list_1 = Alumni.objects.order_by('?')[:3]
    selected=[]
    for i in alumni_list_1:
        selected.append(i.alumni_id)    
    alumni_list_2 = Alumni.objects.exclude(alumni_id__in=selected).order_by('?')[:3]
    for i in alumni_list_2:
        selected.append(i.alumni_id)
    alumni_list_3 = Alumni.objects.exclude(alumni_id__in=selected).order_by('?')[:3]
    return render(req,'Home.html',{'alumni_list_1':alumni_list_1,'alumni_list_2':alumni_list_2,'alumni_list_3':alumni_list_3})

def register(req):
    return render(req,'Register.html')

def otp_modal(request):
    email=request.session.get('email')
    if ('email') in request.session and OTP.objects.filter(email=email).exists():
        return render(request,'Otp_modal.html')
    else:
        return redirect('error_page')
    
def error_page(req):
    return render(req,'Error_page.html')

def registration_form(request):
    email=request.session.get('email')
    if ('email') in request.session and OTP.objects.filter(email=email).exists():
        data={'email':email}
        return render(request,'Registration_form.html',data)
    else:
        return redirect('/')
    
def something_went_wrong(request):
    return render(request,'Something_went_wrong.html')
    
def logout(req):
    try:
        del req.session['email']
    except KeyError:
        pass
    return redirect('/')

# Alumni admin pages   

def admin_home(request):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        bca=Alumni.objects.filter(course="BCA").count()
        cse=Alumni.objects.filter(course="B.Tech-CSE").count()
        aiml=Alumni.objects.filter(course="B.Tech-CSE(AI & ML)").count()
        ece=Alumni.objects.filter(course="B.Tech-ECE").count()
        it=Alumni.objects.filter(course="B.Tech-IT").count()
        ee=Alumni.objects.filter(course="B.Tech-EE").count()
        aeie=Alumni.objects.filter(course="B.Tech-AEIE").count()
        mca=Alumni.objects.filter(course="MCA").count()
        mtech=Alumni.objects.filter(course="M.Tech").count()
        #Chart
        data=[['Dept','Alumni'],['B.Tech-CSE',cse],['B.Tech-CSE(AI & ML)',aiml],['B.Tech-ECE',ece],['B.Tech-IT',it],['B.Tech-EE',ee],['B.Tech-AEIE',aeie],['BCA',bca],['MCA',mca],['M.Tech',mtech]]
        modified_data=json.dumps(data)
        
        total_admin=Coordinator.objects.count()
        total_alumni=Alumni.objects.count()
        details={'bca':bca,'cse':cse,'aiml':aiml,'ece':ece,'it':it,'ee':ee,'aeie':aeie,'mca':mca,'mtech':mtech}
        obj=Coordinator.objects.get(email=email)
        data={'total_admin':total_admin,'total_alumni':total_alumni,'obj':obj.fullname,'details':details,'values':modified_data}
        return render(request,'Admin_home.html',data)
    else:
        return redirect('/#login')
    
def add_admin(request):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        return render(request,'Add_admin.html')
    else:
        return redirect('error_page')
    
def search_alumni(request):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        allData=Alumni.objects.all()
        paginator=Paginator(allData,52)
        page_number=request.GET.get('page',1)
        allDataFinal=paginator.get_page(page_number)
        totalpagenumber=allDataFinal.paginator.num_pages 
        if (int(page_number)<1 or int(page_number)>totalpagenumber):
            return redirect('error_page')
        else:
            start_index = max(int(page_number) - 1, 1)
            end_index = min(start_index + 2, paginator.num_pages) 
            data={'allDataFinal':allDataFinal,'lastpage':totalpagenumber,'totalPageList':list(range(start_index, end_index + 1)),'currentpage':int(page_number),'has_previous': int(page_number) > 1,'has_next': int(page_number) < paginator.num_pages,}
            return render(request,'Alumni_search.html',data)
    else:
        return redirect('error_page')
    
def coordinator_details(request):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        allData=Coordinator.objects.all()
        paginator=Paginator(allData,12)
        page_number=request.GET.get('page',1)
        allDataFinal=paginator.get_page(page_number)
        totalpagenumber=allDataFinal.paginator.num_pages 
        if (int(page_number)<1 or int(page_number)>totalpagenumber):
            return redirect('error_page')
        else:
            start_index = max(int(page_number) - 1, 1)
            end_index = min(start_index + 2, paginator.num_pages) 
            data={'allDataFinal':allDataFinal,'lastpage':totalpagenumber,'totalPageList':list(range(start_index, end_index + 1)),'currentpage':int(page_number),'has_previous': int(page_number) > 1,'has_next': int(page_number) < paginator.num_pages,}
            return render(request,'Coordinator_details.html',data)
    else:
        return redirect('error_page')
    
def edit_admin_otp(request,id):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        obj=Coordinator.objects.get(id=id)
        email=obj.email
        otp=generate_otp()
        data={'record':obj}
        if OTP.objects.filter(email=email).exists():
            OTP.objects.filter(email=email).delete()
            OTP.objects.create(email=email,otp=otp)
        else:
            OTP.objects.create(email=email,otp=otp)
        message=f"\nHello {obj.fullname},\n\nYour OTP for RCCIIT Alumni edit credential process is {otp}.\n\nThanks & Regards,\nRCCIIT Alumni Co-ordinator Team"
        title="OTP for RCCIIT Alumni Edit Admin Credentials"
        do_email(message,title,email)
        return render(request,'Edit_admin_otp.html',data)
    else:
        return redirect('error_page')
    
def edit_credentials(request,id):
    email=request.session.get('email')
    obj=Coordinator.objects.get(id=id)
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists() and OTP.objects.filter(email=obj.email).exists():
        data={'record':obj}
        return render(request,'Edit_credentials.html',data)
    else:
        return redirect('error_page')
    
def delete_credentials(request,id):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        obj=Coordinator.objects.get(id=id)
        obj.delete()
        storage=messages.get_messages(request)
        storage.used=True
        messages.info(request,"Record Has Been Deleted")
        return redirect('/coordinator_details/')
    else:
        return redirect('error_page')

def view_application(request):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        try:
            allData=Application.objects.all()
            count=Application.objects.count()
            paginator=Paginator(allData,52)
            page_number=request.GET.get('page',1)
            allDataFinal=paginator.get_page(page_number)
            totalpagenumber=allDataFinal.paginator.num_pages 
            if (int(page_number)<1 or int(page_number)>totalpagenumber):
                return redirect('error_page')
            else:
                start_index = max(int(page_number) - 1, 1)
                end_index = min(start_index + 2, paginator.num_pages) 
                data={'allDataFinal':allDataFinal,'lastpage':totalpagenumber,'totalPageList':list(range(start_index, end_index + 1)),'currentpage':int(page_number),'has_previous': int(page_number) > 1,'has_next': int(page_number) < paginator.num_pages,'count':count}
                return render(request,'View_application.html',data)
        except:
            return redirect('something_went_wrong')
    else:
        return redirect('error_page')
    
def view_details(request,application_id):
    email=request.session.get('email')
    if ('email' in request.session and Coordinator.objects.filter(email=email).exists()):
        obj=Application.objects.get(application_id=application_id)
        obj.dob=obj.dob.strftime("%d-%b-%Y")
        data={'obj':obj}
        return render(request,'View_details.html',data)
    else:
        return redirect('error_page')
    
def accept_application(request,application_id):
    emailid=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=emailid).exists():
        try:
            obj=Application.objects.get(application_id=application_id)
            name=obj.name
            dob=obj.dob
            phno=obj.phno
            email=obj.email
            password=obj.password
            address=obj.address
            profile_picture=obj.profile_picture
            qualification=obj.qualification
            course=obj.course
            year_of_passing=obj.year_of_passing
            percentage=obj.percentage
            certificate=obj.certificate
            organization_name=obj.organization_name
            doj_month=obj.doj_month
            doj_year=obj.doj_year
            job_profile=obj.job_profile
            job_location=obj.job_location
            linked_in_url=obj.linked_in_url
            Alumni.objects.create(name=name,dob=dob,phno=phno,email=email,password=password,address=address,profile_picture=profile_picture,qualification=qualification,course=course,year_of_passing=year_of_passing,percentage=percentage,certificate=certificate,organization_name=organization_name,doj_month=doj_month,doj_year=doj_year,job_profile=job_profile,job_location=job_location,linked_in_url=linked_in_url)
            message=f"\nHello {name},\n\nYour application with an application id {obj.application_id} has granted and verified successfully.You can login now as an alumni on the website.\n\nThanks & Regards,\nRCCIIT Alumni Management Team"
            title="RCCIIT Alumni Registration"
            do_email(message,title,email)
            obj.delete()
            return redirect('view_application')
        except:
            return redirect('something_went_wrong')
    else:
        return redirect('error_page')
    
def delete_application(request,application_id):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        obj=Application.objects.get(application_id=application_id)
        try:
            media_root=settings.MEDIA_ROOT
            profile_path=os.path.join(media_root,str(obj.profile_picture))
            certificate_path=os.path.join(media_root,str(obj.certificate))
            os.remove(profile_path)
            os.remove(certificate_path)
            obj.delete()
        except:
            return redirect('error_page')
        return redirect('view_application')
    else:
        return redirect('error_page')
    
def search_view_details(request,alumni_id):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        obj=Alumni.objects.get(alumni_id=alumni_id)
        obj.dob=obj.dob.strftime("%d-%b-%Y")
        data={'obj':obj}
        return render(request,'Search_view_details.html',data)
    else:
        return redirect('error_page')
    
def delete_alumni(request,alumni_id):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        obj=Alumni.objects.get(alumni_id=alumni_id)
        try:
            media_root=settings.MEDIA_ROOT
            profile_path=os.path.join(media_root,str(obj.profile_picture))
            certificate_path=os.path.join(media_root,str(obj.certificate))
            os.remove(profile_path)
            os.remove(certificate_path)
            obj.delete()
        except:
            return redirect('error_page')
        return redirect('search_alumni')
    else:
        return redirect('error_page')
    
def change_password_otp(request):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        obj=Coordinator.objects.get(email=email)
        otp=generate_otp()
        if OTP.objects.filter(email=email).exists():
            OTP.objects.filter(email=email).delete()
            OTP.objects.create(email=email,otp=otp)
        else:
            OTP.objects.create(email=email,otp=otp)
        message=f"\nHello {obj.fullname},\n\nYour OTP for Change Password process is {otp}.\n\nThanks & Regards,\nRCCIIT Alumni Co-ordinator Team"
        title="OTP for RCCIIT Admin Change Password"
        do_email(message,title,email)
        data={'record':obj}
        return render(request,'Change_password_otp.html',data)
    else:
        return redirect('error_page')
    
def change_password(request):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        obj=Coordinator.objects.get(email=email)
        data={'record':obj}
        return render(request,'Change_password.html',data)
    else:
        return redirect('error_page')
    
def search_alumni_values(request):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        return render(request,'Search_alumni_values.html')
    else:
        return redirect('error_page')

def search_view_application(request):
    return render(request,'Search_view_application.html')

def admin_news(request):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
        event_obj=Events.objects.all()
        post_obj=Posts.objects.all().order_by('-posted_on')[0:10]
        totalpost_obj=Posts.objects.all().count()
        new_post_obj=[]
        for post in post_obj:
            alumni=Alumni.objects.get(email=post.email)
            if alumni:
                obj={'post_id':post.post_id, 'email':post.email,'posted_on':post.posted_on,'title':post.title,'description':post.description, 'link1':post.link1,'link2':post.link2,'link3':post.link3,'name':alumni.name,'profile_picture':alumni.profile_picture}
                new_post_obj.append(obj)
        data={'event_obj':event_obj, 'post_obj':new_post_obj,'totalpost_obj':totalpost_obj}       
        return render(request,'Admin_news.html',data)
    else:
        return redirect('error_page')

def add_events(request):
    email=request.session.get('email')
    if ('email') in request.session and Coordinator.objects.filter(email=email).exists():   
        return render(request,'Add_events.html')
    else:
        return redirect('error_page')
    
def delete_post_by_admin(request,post_id):
    try:
        email=request.session.get('email')
        if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
            obj=Posts.objects.get(post_id=post_id)
            obj.delete()
            return redirect('admin_news')
    except:
        return redirect('something_went_wrong')
    
def manage_events(request):
    try:
        email=request.session.get('email')
        if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
            obj=Events.objects.all()
            data={'obj':obj}
            return render(request,'Manage_event.html',data)
    except:
        return redirect('something_went_wrong')

def delete_events(request,event_id):
    try:
        email=request.session.get('email')
        if ('email') in request.session and Coordinator.objects.filter(email=email).exists():
            obj=Events.objects.get(event_id=event_id)
            media_root=settings.MEDIA_ROOT
            event_path=os.path.join(media_root,str(obj.event))
            os.remove(event_path)
            obj.delete()
            return redirect('manage_events')
    except:
        return redirect('something_went_wrong')



# Alumni user pages

def alumni_home(request):
    email=request.session.get('email')
    if ('email') in request.session and Alumni.objects.filter(email=email).exists():
        temp_obj=Alumni.objects.get(email=email)
        batchmates_count=Alumni.objects.filter(course=temp_obj.course,year_of_passing=temp_obj.year_of_passing).exclude(email=email).count()
        event_obj=Events.objects.all()
        post_obj=Posts.objects.all().order_by('-posted_on')[0:10]
        alumni_count=Alumni.objects.all().count()
        totalpost_obj=Posts.objects.all().count()
        new_post_obj=[]
        for post in post_obj:
            alumni=Alumni.objects.get(email=post.email)
            if alumni:
                obj={'post_id':post.post_id, 'email':post.email,'posted_on':post.posted_on,'title':post.title,'description':post.description, 'link1':post.link1,'link2':post.link2,'link3':post.link3,'name':alumni.name,'profile_picture':alumni.profile_picture}
                new_post_obj.append(obj)
        data={'event_obj':event_obj, 'post_obj':new_post_obj,'alumni_count':alumni_count,'batchmates_count':batchmates_count,'totalpost_obj':totalpost_obj}
        return render(request,'Alumni_home.html',data)
    else:
        return redirect('error_page')
    
def create_post(request):
    email=request.session.get('email')
    if ('email') in request.session and Alumni.objects.filter(email=email).exists():
        return render(request,'Create_post.html')
    else:
        return redirect('error_page')
    
def my_profile(request):
    email=request.session.get('email')
    if ('email') in request.session and Alumni.objects.filter(email=email).exists():
        data_obj=Alumni.objects.get(email=email)
        post_obj=Posts.objects.filter(email=email).order_by('-posted_on')[:5]
        totalpost_obj=Posts.objects.filter(email=email).count()
        data_obj.dob=data_obj.dob.strftime("%d-%b-%Y")
        data={'data_obj':data_obj,'post_obj':post_obj,'totalpost_obj':totalpost_obj}
        return render(request,'My_profile.html',data)
    else:
        return redirect('error_page')
    
def edit_posts(request,post_id):
    email=request.session.get('email')
    if ('email') in request.session and Alumni.objects.filter(email=email).exists():
        obj=Posts.objects.get(post_id=post_id)
        data={'obj':obj}
        return render(request,'Edit_post.html',data)
    else:
        return redirect('error_page')
    
def batchmates(request):
    email=request.session.get('email')
    if ('email') in request.session and Alumni.objects.filter(email=email).exists():
        obj=Alumni.objects.get(email=email)
        allData=Alumni.objects.filter(course=obj.course,year_of_passing=obj.year_of_passing)
        allData1=allData.exclude(email=email)
        paginator=Paginator(allData1,52)
        page_number=request.GET.get('page',1)
        allDataFinal=paginator.get_page(page_number)
        totalpagenumber=allDataFinal.paginator.num_pages 
        if (int(page_number)<1 or int(page_number)>totalpagenumber):
            return redirect('error_page')
        else:
            start_index = max(int(page_number) - 1, 1)
            end_index = min(start_index + 2, paginator.num_pages) 
            data={'allDataFinal':allDataFinal,'lastpage':totalpagenumber,'totalPageList':list(range(start_index, end_index + 1)),'currentpage':int(page_number),'has_previous': int(page_number) > 1,'has_next': int(page_number) < paginator.num_pages,'count':len(allDataFinal)}
            return render(request,'Batchmates.html',data)
    else:
        return redirect('error_page')
    
def alumni_search_alumni(request):
    email=request.session.get('email')
    if ('email') in request.session and Alumni.objects.filter(email=email).exists():
        return render(request,'Alumni_search_alumni.html')
    else:
        return redirect('error_page')

    
def edit_profile(request):
    email=request.session.get('email')
    if ('email') in request.session and Alumni.objects.filter(email=email).exists():
        obj=Alumni.objects.get(email=email)
        data={'obj':obj}
        return render(request,'Edit_profile.html',data)
    else:
        return redirect('error_page')

def alumni_change_password(request):
    email=request.session.get('email')
    if ('email') in request.session and Alumni.objects.filter(email=email).exists() and OTP.objects.filter(email=email).exists():
        obj=Alumni.objects.get(email=email)
        data={'record':obj}
        return render(request,'Alumni_change_password.html',data)
    else:
        return redirect('error_page')
    
def alumni_change_password_otp(request):
    email=request.session.get('email')
    if ('email') in request.session and Alumni.objects.filter(email=email).exists():
        obj=Alumni.objects.get(email=email)
        otp=generate_otp()
        if OTP.objects.filter(email=email).exists():
            OTP.objects.filter(email=email).delete()
            OTP.objects.create(email=email,otp=otp)
        else:
            OTP.objects.create(email=email,otp=otp)
        message=f"\nHello {obj.name},\n\nYour OTP for Change Password process is {otp}.\n\nThanks & Regards,\nRCCIIT Alumni Management Team"
        title="OTP for RCCIIT Alumni Change Password"
        do_email(message,title,email)
        data={'record':obj}
        return render(request,'Alumni_change_password_otp.html',data)
    else:
        return redirect('error_page')
    
def search_people(request):
    return render(request,'Search_people.html')

    
# Rest APIs(Common and Admin)

def get_otp(request):
    if request.method=='POST':
        email=request.POST["email"]
        if Application.objects.filter(email=email).exists() or Alumni.objects.filter(email=email).exists():
            storage=messages.get_messages(request)
            storage.used=True
            messages.info(request,"Email already exists in an application")
            return render(request,'Register.html')
        else:
            otp=generate_otp()
            if OTP.objects.filter(email=email).exists():
                OTP.objects.filter(email=email).delete()
                OTP.objects.create(email=email,otp=otp)
            else:
                OTP.objects.create(email=email,otp=otp)
            request.session['email']=email
            message=f"\nHello User,\n\nYour OTP for RCCIIT Alumni Registration process is {otp}.\n\nThanks & Regards,\nRCCIIT Alumni Management Team"
            title="OTP for RCCIIT Alumni Registration"
            do_email(message,title,email)
            return render (request,'Otp_modal.html')
    else:
        return redirect('error_page')
    
def verify_otp(request):
    if request.method=='POST':
        email=request.session.get('email')
        otp=request.POST['otp']
        storage=messages.get_messages(request)
        storage.used=True
        obj=OTP.objects.filter(email=email,otp=otp)
        if len(obj)>0:
            return redirect('registration_form')
        else:
            messages.info(request,"OTP is not correct")
            return render(request,'Otp_modal.html')
    else:
        return redirect('error_page')    

def admin_login_verification(request):
    email=request.POST['email']
    password=request.POST['password']
    storage=messages.get_messages(request)
    storage.used=True
    if(Coordinator.objects.filter(email=email).exists()):
        if(Coordinator.objects.filter(email=email,password=password)):
            request.session['email']=email
            return redirect('admin_home')
        else:
            messages.info(request,"Username or password does not match")
            return redirect('/#login')
    else:
        messages.info(request,"Username or password does not match")
        return redirect('/#login')

def add_alumni_coordinator(request):
    if request.method=='POST':
        fullname=request.POST['fullname']
        email=request.POST['email']
        password=request.POST['password']
        storage=messages.get_messages(request)
        storage.used=True
        if(Coordinator.objects.filter(email=email).exists()):
            messages.info(request,"Email already exists")
        else:
            Coordinator.objects.create(email=email,fullname=fullname,password=password)
            messages.info(request,"Record Added Successfully")
            message=f"\nHello {fullname},\n\nYour password for Admin of RCCIIT Alumni  is {password}.\n\nThanks & Regards,\nRCCIIT Alumni Co-ordinator Team"
            title="Your Admin Credentials for RCCIIT Alumni"
            do_email(message,title,email)
        return render(request,'Add_admin.html')
    else:
        return redirect('error_page')
    
def search_details(request):
    if request.method=='POST':
        search_by=request.POST['search_by']
        search=request.POST['search']
        storage=messages.get_messages(request)
        storage.used=True
        if(search_by=="all"):
            return redirect('search_alumni')
        elif(search_by=="name"):
            allData=Alumni.objects.filter(Q(name__icontains=search))
        elif(search_by=="course"):
            allData=Alumni.objects.filter(Q(course__icontains=search))
        elif(search_by=="passing year"):
            allData=Alumni.objects.filter(Q(year_of_passing__icontains=search))
        elif(search_by=="alumni id"):
            allData=Alumni.objects.filter(Q(alumni_id__icontains=search))
        elif(search_by=="email"):
            allData=Alumni.objects.filter(Q(email__icontains=search))
        elif(search_by=="organization"):
            allData=Alumni.objects.filter(Q(organization_name__icontains=search))
        elif(search_by=="job role"):
            allData=Alumni.objects.filter(Q(job_profile__icontains=search))
        if(allData.count()>0):
            data={'allDataFinal':allData,'match_count':len(allData)}
            return render(request,'Search_alumni_values.html',data)
        else:
            messages.info(request,"No records found")
            return redirect('search_alumni')
    else:
        return redirect('error_page')
        
def search_admin(request):
    if request.method=='POST':
        search_by=request.POST['search_by']
        search=request.POST['search']
        storage=messages.get_messages(request)
        storage.used=True
        if(search_by=="all"):
            return redirect('coordinator_details')
        elif(search_by=="name"):
            allData=Coordinator.objects.filter(Q(fullname__icontains=search))
        elif(search_by=="email"):
            allData=Coordinator.objects.filter(Q(email__icontains=search))
        else:
            allData=Coordinator.objects.all()
        data={'allData':list(allData)}
        if (len(data['allData'])):
            return render(request,'Search_admin_values.html',data)
        else:
            messages.info(request,"No records found")
            return redirect('coordinator_details')
    else:
        return redirect('error_page')
    
def edit_admin_verify_otp(request):
    if request.method=='POST':
        id=request.POST['id']
        obj=Coordinator.objects.get(id=id)
        email=obj.email
        otp=request.POST['otp']
        storage=messages.get_messages(request)
        storage.used=True
        obj1=OTP.objects.filter(email=email,otp=otp)
        if len(obj1)>0:
            return redirect('/edit_credentials/'+id)
        else:
            messages.info(request,"OTP is not correct")
            return redirect('/edit_admin_otp/'+id)
    else:
        return redirect('error_page')

def update_admin_credentials(request):
    if request.method=='POST':
        id=request.POST['id']
        fullname=request.POST['fullname']
        emailid=request.POST['email']
        password=request.POST['password']
        storage=messages.get_messages(request)
        storage.used=True
        obj=Coordinator.objects.get(id=id)
        obj.fullname=fullname
        obj.email=emailid
        obj.password=password
        obj.save()
        otp=OTP.objects.get(email=emailid)
        otp.delete()
        messages.info(request,"Record Updated Successfully")
        return redirect('/coordinator_details/')
    else:
        return redirect('error_page') 

def save(request):
    if request.method == 'POST':
        try:
            name=request.POST['name']
            dob=request.POST['dob']
            phno=request.POST['phno']
            email=request.POST['email']
            password=request.POST['password']
            address=request.POST['address']
            profile_picture=request.FILES['profile_picture']
            qualification=request.POST['qualification']
            course=request.POST['course']
            year_of_passing=request.POST['year_of_passing']
            percentage=request.POST['percentage']
            certificate=request.FILES['certificate']
            organization_name=request.POST['organization_name']
            doj_month=request.POST['doj_month']
            doj_year=request.POST['doj_year']
            job_profile=request.POST['job_profile']
            job_location=request.POST['job_location']
            linked_in_url=request.POST['linked_in_url']
            obj=Application.objects.create(name=name,dob=dob,phno=phno,email=email,password=password,address=address,profile_picture=profile_picture,qualification=qualification,course=course,year_of_passing=year_of_passing,percentage=percentage,certificate=certificate,organization_name=organization_name,doj_month=doj_month,doj_year=doj_year,job_profile=job_profile,job_location=job_location,linked_in_url=linked_in_url)
            message=f"\nHello {name},\n\nYou have successfully registered for the RCCIIT Alumni registration with an application id {obj.application_id}.You can track your application status on the website\n\nThanks & Regards,\nRCCIIT Alumni Management Team"
            title="RCCIIT Alumni Registration"
            do_email(message,title,email)
            obj=OTP.objects.filter(email=email)
            obj.delete()
            try:
                del request.session['email']
            except KeyError:
                pass
            return redirect('/')
        except:
            return redirect('something_went_wrong')
    else:
        return redirect('error_page')   
    
def search_by_id(request):
    if request.method=='POST':
        try:
            search=request.POST['search']
            storage=messages.get_messages(request)
            storage.used=True
            allData=Application.objects.filter(Q(application_id__contains=search))
            data={'allData':list(allData)}
            if len(data['allData'])>0:
                return render(request,'Search_view_application.html',data)
            else:
                messages.info(request,"No records found")
                return redirect('view_application')
        except:
            return redirect('error_page')
    else:
        return redirect('error_page')
    
def change_password_otp_verify(request):
    if request.method=='POST':
        email=request.session.get('email')
        otp=request.POST['otp']
        storage=messages.get_messages(request)
        storage.used=True
        if OTP.objects.filter(email=email,otp=otp):
            return redirect('change_password')
        else:
            messages.info(request,"OTP does not match")
            return render(request,'Change_password_otp.html')
    else:
        return redirect('error_page')
    
def update_password(request):
    if request.method=='POST':
        email=request.session.get('email')
        password=request.POST['password']
        if Coordinator.objects.filter(email=email).exists():
            obj=Coordinator.objects.get(email=email)
            obj.password=password
            obj.save()
            otp=OTP.objects.get(email=email)
            otp.delete()
            return redirect('admin_home')
        else:
            return redirect('error_page')
        
def create_event(request):
    try:
        email=request.session.get('email')
        if request.method=='POST' and Coordinator.objects.filter(email=email).exists():
            posted_on=request.POST['posted_on']
            description=request.POST['description'] 
            poster=request.FILES['poster']
            is_new=request.POST['is_new']
            Events.objects.create(posted_on=posted_on,description=description,event=poster,is_new=is_new)
            return redirect('admin_news')
    except:
        return redirect('something_went_wrong') 

#REST APIs (Alumni Only)

def alumni_login_verification(request):
    try:
        email=request.POST['email']
        password=request.POST['password']
        storage=messages.get_messages(request)
        storage.used=True
        if(Alumni.objects.filter(email=email).exists()):
            if(Alumni.objects.filter(email=email,password=password)):
                request.session['email']=email
                return redirect('alumni_home')
            else:
                messages.info(request,"Username or password does not match")
                return redirect('/#login')
        else:
            messages.info(request,"Username or password does not match")
            return redirect('/#login')
    except:
        return redirect('something_went_wrong')
    
def insert_post(request):
    try:
        if request.method=='POST':
            email=request.session.get('email')
            if ('email') in request.session and Alumni.objects.filter(email=email).exists():
                posted_on=request.POST['posted_on']
                title=request.POST['title']
                description=request.POST['description']
                link1=request.POST['link1']
                link2=request.POST['link2']
                link3=request.POST['link3']
                Posts.objects.create(email=email,posted_on=posted_on,title=title,description=description,link1=link1,link2=link2,link3=link3)
                return redirect('alumni_home')
            else:
                return redirect('error_page')
        else:
            return redirect('error_page')
    except:
        return redirect('something_went_wrong')

def edit_post(request):
    try:
        if request.method=='POST':
            email=request.session.get('email')
            if ('email') in request.session and Alumni.objects.filter(email=email).exists():
                post_id=request.POST['post_id']
                title=request.POST['title']
                description=request.POST['description']
                link1=request.POST['link1']
                link2=request.POST['link2']
                link3=request.POST['link3']
                obj=Posts.objects.get(post_id=post_id)
                obj.title=title
                obj.description=description
                obj.link1=link1
                obj.link2=link2
                obj.link3=link3
                obj.save()
                return redirect('my_profile')
    except:
        return redirect('something_went_wrong')
    
def delete_post(request,post_id):
    try:
        email=request.session.get('email')
        if ('email') in request.session and Alumni.objects.filter(email=email).exists():
            obj=Posts.objects.get(post_id=post_id)
            obj.delete()
            return redirect('my_profile')
    except:
        return redirect('something_went_wrong')

def update_profile(request):
    try:
        email=request.session.get('email')
        if request.method=='POST':
            obj=Alumni.objects.get(email=email)
            phno=request.POST['phno']
            address=request.POST['address']
            year_of_passing=request.POST['year_of_passing']
            organization_name=request.POST['organization_name']
            doj_month=request.POST['doj_month']
            doj_year=request.POST['doj_year']
            job_profile=request.POST['job_profile']
            job_location=request.POST['job_location']
            linked_in_url=request.POST['linked_in_url']
            obj.phno=phno
            obj.address=address
            obj.year_of_passing=year_of_passing
            obj.organization_name=organization_name
            if doj_month=='' or doj_year=='':
                if doj_month!='':
                    obj.doj_month=doj_month
                elif doj_year!='':
                    obj.doj_year=doj_year
            elif doj_month!='' and doj_year!='':
                obj.doj_month=doj_month
                obj.doj_year=doj_year
            obj.job_profile=job_profile
            obj.job_location=job_location
            obj.linked_in_url=linked_in_url
            obj.save()
            return redirect('my_profile')
        else:
            return redirect('error_page')
    except:
        return redirect('something_went_wrong')
    
def update_profile_picture(request):
    try:
        email=request.session.get('email')
        if request.method=='POST' and ('email') in request.session and Alumni.objects.filter(email=email).exists():
            temp=Alumni.objects.get(email=email)
            profile_picture=request.FILES['profile_picture']
            os.remove('media/'+str(temp.profile_picture))
            temp.profile_picture=profile_picture
            temp.save()
            return redirect('my_profile')
        else:
            return redirect('error_page')       
    except:
        return redirect('something_went_wrong')

def alumni_change_password_otp_verify(request):
    if request.method=='POST':
        email=request.session.get('email')
        otp=request.POST['otp']
        storage=messages.get_messages(request)
        storage.used=True
        if OTP.objects.filter(email=email,otp=otp):
            return redirect('/alumni_change_password/')
        else:
            messages.info(request,"OTP does not match")
            return render(request,'Alumni_change_password_otp.html')
    else:
        return redirect('error_page')
    
def alumni_update_password(request):
    if request.method=='POST':
        email=request.session.get('email')
        password=request.POST['password']
        if Alumni.objects.filter(email=email).exists():
            obj=Alumni.objects.get(email=email)
            obj.password=password
            obj.save()
            otp=OTP.objects.get(email=email)
            otp.delete()
            return redirect('alumni_home')
        else:
            return redirect('error_page')

def alumni_search_people(request):
    if request.method=='POST':
        search_by=request.POST['search_by']
        search=request.POST['search']
        storage=messages.get_messages(request)
        storage.used=True
        if(search_by=="name"):
            allData=Alumni.objects.filter(Q(name__icontains=search))
        elif(search_by=="course"):
            allData=Alumni.objects.filter(Q(course__icontains=search))
        elif(search_by=="passing year"):
            allData=Alumni.objects.filter(Q(year_of_passing__icontains=search))
        elif(search_by=="department"):
            allData=Alumni.objects.filter(Q(course__icontains=search))
        elif(search_by=="email"):
            allData=Alumni.objects.filter(Q(email__icontains=search))
        elif(search_by=="organization"):
            allData=Alumni.objects.filter(Q(organization_name__icontains=search))
        if(allData.count()>0):
            data={'allDataFinal':allData,'count':len(allData)}
            return render(request,'Search_people.html',data)
        else:
            messages.info(request,"No records found")
            return redirect('alumni_search_alumni')
    else:
        return redirect('error_page')



# Other functions

def do_email(message,title,email):
    send_mail(title,message,'settings.EMAIL_HOST_USER',[email],fail_silently=False)

def generate_otp():
    otp = str(random.randint(100000, 999999))
    return otp

# load more function

def  load_more(request):
    offset = request.GET.get('offset')
    offset_int = int(offset)
    limit = 10
    post_obj=Posts.objects.all().order_by('-posted_on')[offset_int:offset_int+limit]
    new_post_obj=[]
    for post in post_obj:
        alumni=Alumni.objects.get(email=post.email)
        if alumni:
            obj={'post_id':post.post_id, 'email':post.email,'posted_on':post.posted_on,'title':post.title,'description':post.description, 'link1':post.link1,'link2':post.link2,'link3':post.link3,'name':alumni.name,'profile_picture':alumni.profile_picture.url}
            new_post_obj.append(obj)
    data={'post_obj':new_post_obj}
    return JsonResponse(data=data,safe=False)

def  my_profile_load_more(request):
    email=request.session.get('email')
    offset = request.GET.get('offset')
    offset_int = int(offset)
    limit = 10
    post_obj=Posts.objects.filter(email=email).order_by('-posted_on')[offset_int:offset_int+limit]
    data_list = list(post_obj.values())
    data={'post_obj':data_list}
    return JsonResponse(data=data,safe=False)

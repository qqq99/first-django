from django.shortcuts import render
from basic_app.forms import UserProfileInfoForm,UserForm
from django.urls import reverse
#decorator:if you want a view require user login, you can decorator it with login_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("YOU ARE logged in, NICE")

@login_required
def user_logout(request):
    #builtin func automatically logout user
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    #aassume first user not registered
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            #save directed to database
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            #make sure set up one to one relationship
            #to prevent overide the user
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form=UserProfileInfoForm()
        #registered = True
    return render(request,'basic_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


#new view, make sure views跟import的东西不重名
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
    
        if user:
            if user.is_active:
                login(request,user)
                #redirect to home page
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("account not active!")
        else:
            print("hi, someone try to login but failed")
            print("Username:{} and password{}".format(username,password))
            return HttpResponse("invalid login")
    else:
        return render(request,'basic_app/login.html',{})
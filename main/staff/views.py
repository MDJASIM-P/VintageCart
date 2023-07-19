from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, CreateView, DeleteView, FormView, ListView, UpdateView
from django.contrib import messages
from product.models import *
from sellers.models import *
from product.forms import *
from sellers.forms import FeedbackForm
from django.utils.decorators import method_decorator
from sellers.views import signin_required

# Create your views here.

def staffonly(fun):
    def inner(request, *args, **kwargs):
        if request.user.is_staff:
            return fun(request, *args, **kwargs)
        else:
            messages.error(request, "U are not a Staff")
            return redirect("index")
    return inner

# Only for Staff 
@method_decorator(staffonly, name="dispatch")
class AddCloth(View):
    def get(self, request, *args, **kwargs):
        form = ClothForm()
        return render(request, "addcloth.html", {"form":form})
    def post(self, request, *args, **kwargs):
        form_data = ClothForm(data= request.POST, files= request.FILES)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, "Added")
            form = ClothForm()
            # return render(request, "addcloth.html", {"form":form})
            return redirect('index')
        else:
            messages.warning(request, "Something went error")
            return render(request, "addcloth.html", {"form":form_data})
        
@method_decorator(staffonly, name="dispatch")      
class UpdateCloth(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pid')
        pro = ClothModel.objects.get(id = id)
        form = ClothForm(instance=pro)
        return render(request, "updatecloth.html", {'form':form})
    def post(self, request, *args, **kwargs):
        id = kwargs.get('pid')
        pro = ClothModel.objects.get(id = id)
        form_data = ClothForm(data=request.POST, files=request.FILES, instance=pro)   
        if form_data.is_valid():
            if 'update' in request.POST:
                form_data.save()
                form = ClothForm()
                messages.success(request, "Cloth Updated")
                # return render(request, "updatecloth.html", {'form':form})
                return redirect('index')
            elif 'delete' in request.POST:
                pro.delete()
                form = ClothForm()
                messages.info(request, "Cloth Deleted")
                # return render(request, "updatecloth.html", {'form':form}) 
                return redirect('index')        
        else:
            return render(request, "updatecloth.html", {'form':form_data})    



def adminOnly(fun):
    def inner(request, *args, **kwargs):
        if request.user.is_superuser:
            return fun(request, *args, **kwargs)
        else:
            messages.error(request, "U are a Fraud")
            return redirect("admn")
    return inner
# Admin Login
from sellers.forms import SellerLogInForm
from django.contrib.auth import authenticate, login, logout
class AdminLogIn(View):
    def get(self, request, *args, **kwargs):
        form = SellerLogInForm()
        return render(request, "admin_login.html", {'form':form})
    def post(self, request, *args, **kwargs):
        form_data = SellerLogInForm(data=request.POST)
        if form_data.is_valid():
            uname = form_data.cleaned_data.get('username')
            psw = form_data.cleaned_data.get('password')
            user = authenticate(request, username=uname, password=psw)
            if user.is_superuser == True:
                login(request, user)
                messages.success(request, 'Login succesfull')
                return redirect('dash')
            else:
                messages.error(request, "Invalid username or Password")
                return render(request, 'admin_login.html', {'form':form_data})
        else:
            return render(request, 'admin_login.html', {'form':form_data})      
@method_decorator(adminOnly, name="dispatch")
class AdminLogOut(View):
    def get(self, request):
        logout(request)
        return redirect('admn')
@method_decorator(adminOnly, name="dispatch")
class AdmView(TemplateView):
    template_name = "admin.html"
@method_decorator(adminOnly, name="dispatch")
class AdmUsrView(TemplateView):
    template_name = "admin_U.html"
@method_decorator(adminOnly, name="dispatch")
class AdmProView(TemplateView):
    template_name = 'admin_P.html'
@method_decorator(adminOnly, name="dispatch")
class AdmMsgView(TemplateView):
    template_name = 'admin_M.html'
@method_decorator(adminOnly, name="dispatch")
class AdmFeedView(TemplateView):
    template_name = 'admin_F.html'
# Message Section
@adminOnly
def admDeleteMessage(self, *args, **kwargs):
    id =  kwargs.get("id")
    msg = MessageModel.objects.get(id=id)
    msg.delete()
    return redirect('admM')
# Feedback Section
@method_decorator(adminOnly, name="dispatch")
class AdmFeedEdit(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        feed = FeedbackModel.objects.get(id=id)
        form = FeedbackForm(instance=feed)
        return render(request, "editfeed.html", {"form":form})
    def post(self, request, *args, **kwargs):
        id = kwargs.get("id")
        feed = FeedbackModel.objects.get(id=id)
        form_data = FeedbackForm(data=request.POST, instance=feed)
        if form_data.is_valid():
            form_data.save()
            return redirect('admF')
        else:
            messages.error(request,"something went wrong!")
            return render(request, "editfeed.html", {"form":form_data})
@adminOnly
def admFeedDelete(self, *args, **kwargs):
    id = kwargs.get("id")
    feed = FeedbackModel.objects.get(id=id)
    feed.delete()
    return redirect("admF")
@adminOnly
def admDeleteReport(self, *args, **kwargs):
    id = kwargs.get("id")
    feed = FeedbackModel.objects.get(id=id)
    Report.objects.filter(feedback=feed).delete()
    return redirect("admF")
# Staff Section
@method_decorator(adminOnly, name="dispatch")
class CreateStaff(View):
    def get(self, request):
        return render(request, "c_staff.html")
    def post(self, request):
        fname = request.POST.get("first_name")
        lname = request.POST.get("last_name")
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pswd = request.POST.get("pssword")
        User.objects.create_user(first_name=fname, last_name=lname, username=uname, email=email, password=pswd, is_staff=True)
        return redirect('dash')
@adminOnly
def makeStaff(self, *args, **kwargs):
    id = kwargs.get('id')
    user = User.objects.get(id=id)
    user.is_staff=True
    user.save()
    return redirect('admU')
@adminOnly
def deleteStaff(self, *args, **kwargs):
    id = kwargs.get('id')
    user = User.objects.get(id=id)
    user.is_staff=False
    user.save()
    return redirect('admU')
@adminOnly
def activateUser(self, *args, **kwargs):
    id = kwargs.get('id')
    user = User.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect('admU')
@adminOnly
def deactivateUser(self, *args, **kwargs):
    id = kwargs.get('id')
    user = User.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect('admU')
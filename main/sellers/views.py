from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import View
from .forms import *
from product.forms import ClothForm
from django.contrib import messages
from .models import *
from product.models import ClothModel, Cart
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.urls import reverse

# created a decorator for signin required
def signin_required(fun):
    def inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return fun(request, *args, **kwargs)
        else:
            messages.error(request, "Login required for this action.")
            return redirect("index")
    return inner
   
class Index(View):
    def get(slef, request, *args, **kwargs):
        user = request.user
        print(user)
        # Checking for valid user or AnonymousUser
        if user.id == None:
            form = MessageForm()
        elif user:
            # auto fill 'email' by user email
            form = MessageForm(initial={'email':user.email})
        form1 = FeedbackForm()
        data = ClothModel.objects.all()
        print(data)
        return render(request, "index.html", {'form':form, 'form1':form1, 'data':data, })
        # return render(request, "index.html")
    def post(self, request, *args, **kwargs):
        if 'msgbtn' in request.POST:
            msgform = MessageForm(data = request.POST)
            if msgform.is_valid():
                msgform.save()
                messages.success(request, "Message sent")
                return redirect('index')
            else:
                messages.error(request, "Invalid Message data")
                return redirect('index')
        elif 'feedbtn' in request.POST:
            user = request.user
            print(user)
            # checking the user
            if user.is_anonymous == True:
                messages.error(request, "U are not an user")
                return redirect('index')
            else:
                pro_id = request.POST.get("demo")
                print(pro_id)
                # current product
                prod = ClothModel.objects.get(id=pro_id)
                feedform = FeedbackForm(data = request.POST)
                if feedform.is_valid():
                    feed = request.POST.get('feedback')
                    title = request.POST.get('title')
                    FeedbackModel.objects.create(pro=prod, seller=user, feedback =feed, datetime = datetime.now(), title=title)               
                    messages.success(request, "Feedback saved")
                    return redirect('index')
                else:
                    messages.error(request, "Invalid Feedback data")
                    return redirect('index')
        else:
            messages.warning(request, "Nothing Happend")
            return redirect('index')
@method_decorator(signin_required, name='dispatch')                   
class ProLike(View):
    def post(self, request, *args, **kwargs):
        pro = get_object_or_404(ClothModel, id=request.POST.get("post_id"))
        if request.user in pro.likes.all():
            pro.likes.remove(request.user)
        else:
            pro.likes.add(request.user)
        return HttpResponseRedirect(reverse('index'))

class SignUp(View):
    def get(self, request, *args, **kwargs):
        form = SellerSignUpForm()
        return render(request, "signup.html", {'form':form})
    def post(self, request, *args, **kwargs):
        form_data = SellerSignUpForm(data=request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('index')
        else:
            return render(request, 'signup.html', {'form':form_data})

from django.contrib.auth import authenticate, login, logout
class LogIn(View):
    def get(self, request, *args, **kwargs):
        form = SellerLogInForm()
        return render(request, "login.html", {'form':form})
    def post(self, request, *args, **kwargs):
        form_data = SellerLogInForm(data=request.POST)
        if form_data.is_valid():
            uname = form_data.cleaned_data.get('username')
            psw = form_data.cleaned_data.get('password')
            user = authenticate(request, username=uname, password=psw)
            if user:
                login(request, user)
                print(user)
                messages.success(request, 'Login succesfull')
                return redirect('index')
            else:
                messages.error(request, "Invalid username or Password")
                return render(request, 'login.html', {'form':form_data})
        else:
            return render(request, 'login.html', {'form':form_data})      

@method_decorator(signin_required, name='dispatch')
class LogOut(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')
    
@method_decorator(signin_required, name='dispatch')  
class ProDetail(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pid')
        pro = ClothModel.objects.get(id=id)
        feed = FeedbackModel.objects.filter(pro=pro).order_by("datetime").reverse()
        rpts = Report.objects.values("feedback")
        print(rpts)
        return render(request, 'prodetail.html', {'pro':pro, 'feed':feed})
    def post(self, request, *args, **kwargs):
        if 'cart' in request.POST:
            id = kwargs.get('pid')
            pro = ClothModel.objects.get(id=id)
            count = request.POST.get("quantity") or 1
            # Checking the same product on Cart
            if Cart.objects.filter(product = pro, user=request.user):
                p = Cart.objects.get(product = pro, user=request.user)
                p.quantity = count
                p.save()
            else:
                Cart.objects.create(product =pro, user=request.user, quantity=count)
            objs = Cart.objects.filter(user=request.user)
            sum = 0
            for i in objs:
                sum += (i.product.price * i.quantity)
            num = len(objs)
            return render(request, 'addcart.html', {"objs":objs, "sum":sum, "num":num})
        elif 'rpt' in request.POST:
            feed = request.POST.get("feedid")
            feed = FeedbackModel.objects.get(id=feed)
            rpt = request.POST.get("report")
            print(rpt)
            if rpt=="None":
                messages.error(request, "Select a report")
                return redirect("detail", **kwargs)
            else:
                Report.objects.create(feedback=feed, report=rpt, user=request.user.id)
                return redirect("detail", **kwargs)
            
        
# Feedback Section  
@signin_required
def feedLike(request, *args, **kwargs):
    feed = get_object_or_404(FeedbackModel, id=kwargs.get("id"))
    if request.user in feed.likes.all():
        feed.likes.remove(request.user)
    else:
        feed.likes.add(request.user)
    return redirect('detail', pid=feed.pro.id)
@method_decorator(signin_required, name='dispatch') 
class FeedEdit(View):
    def get(self, request,*args, **kwargs):
        feed = get_object_or_404(FeedbackModel, id=kwargs.get("id"))
        form = FeedbackForm(instance=feed)
        return render(request, 'feedEdit.html', {"form":form})
    def post(self, request, *args, **kwargs):
        feed = get_object_or_404(FeedbackModel, id=kwargs.get("id"))
        form_data = FeedbackForm(data=request.POST, instance=feed)
        if form_data.is_valid():
            form_data.save()
            return redirect("detail", pid=feed.pro.id)
        else:
            return render(request, 'feedEdit.html', {"form":form_data})
@signin_required
def feedRemove(self, *args, **kwargs):
    id=kwargs.get("id")
    feed = FeedbackModel.objects.get(id=id)
    feed.delete()
    return redirect('detail', pid=feed.pro.id)


@method_decorator(signin_required, name='dispatch')  
class CartView(View):
    def get(self, request, *args, **kwargs):
        objs = Cart.objects.filter(user=request.user)
        sum = 0
        for i in objs:
            sum += (i.product.price * i.quantity)
        num = len(objs)
        return render(request, 'addcart.html', {"objs":objs, "sum":sum, "num":num})


        


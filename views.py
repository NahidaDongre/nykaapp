from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Product,Brand
import razorpay

from django.db.models import Q
from .forms import UserForm, UserProfileForm
from .models import Cart,Order,UserProfile
# Create your views here.
def home(request):
    context={}
    p=Product.objects.all()
    context["products"]=p

    print("my current request id id",request.user.id)
    return render(request,"index.html",context)

def cart(request):
    p = Product.objects.all()
    return render(request,"cart.html")

def brandcart(request):
    return render(request,"brandcart.html")

def Categories(request):
    context={}
    p=Brand.objects.all()
    context['brands']=p
    return render(request,"Categories.html",context)

def contact(request):
    return render(request,"contact.html")


def about(request):
    return render(request,"about.html")

def register(request):
    context={}
    if request.method=="GET":
        return render(request,"register.html")
    else:
        nm=request.POST["uname"]
        p=request.POST["pass"]
        cp=request.POST["cpass"]
        print(nm,p,cp)
        if nm =='' or p=="" or cp=="":
            context["errmsg"]="fields can not be empty"
            return render(request,"register.html",context)

        elif p!=cp:
            context["errmsg"]="p and cp not matching "
            return render(request,"register.html",context)

        else:
            #obj=model.objects.create(colnames=values)# Query set
            context["success"]="Registration successful please login now"
            u=User.objects.create(username=nm,email=nm)
            u.set_password(p)
            u.save()
            return render(request,"register.html",context)


def ulogin(request):
    context={}
    if request.method=='POST':
        un=request.POST["uname"]
        p=request.POST["pass"]
               

        if un=="" or p=="":
            context["errmsg"]="fields can not be empty"
            return render(request,"login.html")
        else:   
            u=authenticate(username=un,password=p)
            print(u)
            if u is not None:
                login(request,u)
                return redirect("/home")
            else:
                context["errmsg"]="Username and Password Not Matched"
                return render(request,"login.html",context)
    else:
        return render(request,"login.html")

def ulogout(request):
    logout(request)
    return redirect("/home")

def catfilter(request,cv):
    p=Product.objects.filter(category=cv)
    context={}
    context["products"]=p
    return render(request,"index.html",context)

def sortbyprice(request,sp):
    if sp =="0":
        p=Product.objects.order_by("-price").filter(is_active=True)
    else:
        p=Product.objects.order_by("price").filter(is_active=True)
    context={}
    context["products"]=p
    return render(request,"index.html",context)   
  
def filterbyprice(request):
    mx=request.GET['maxi']
    nm=request.GET['min']
    q1=Q(price__gte=nm)
    q2=Q(price__lte=mx)
    p=Product.objects.filter(q1 & q2)
    context={}
    context["products"]=p
    return render(request,"index.html",context)


def productsdetail(request,rid):
    p=Product.objects.filter(id=rid)
    context={}
    context["products"]=p
    return render(request,"productsdetail.html",context)

def viewcart(request):
    context={}
    c=Cart.objects.filter(userid=request.user.id)
    context["carts"]=c
    sum=0
    for i in c:
        sum=i.pid.price*i.qty
    context["total"]=sum

    return render(request,"cart.html",context)

def addtocart(request,pid):
    context={}
    if request.user.is_authenticated:
        u=User.objects.filter(id=request.user.id)
        p=Product.objects.filter(id=pid)
        q1=Q(userid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        if n==1:
            context["msg"]="Product already exist in cart"
            return render(request,"productsdetail.html",context)
        else:
            cart=Cart.objects.create(userid=u[0],pid=p[0])
            cart.save()
            context["msg"]="Product added in cart successfuly"
            return render(request,"productsdetail.html",context)
    else:
        return redirect("/login")
   
def removecart(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    context={}
    context["remove"]="Product Removed from Cart"
    return render(request,"cart.html",context)


   
def updateqty(request,x,cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    if x=="1":
        q=q+1
    elif q>1:
        q=q-1
    c.update(qty=q)
    return redirect('/viewcart')

def branddetail(request,bid):
    p=Brand.objects.filter(id=bid)
    context={}
    context["brands"]=p
    return render(request,"branddetail.html",context)

def brand(request):
    context={}
    p=Brand.objects.all()
    context["brands"]=p
    return render(request,"Categories.html",context)

import random
def placeorder(request):
        c=Cart.objects.filter(userid=request.user.id)
        orderid=random.randrange(1000,9999)
        for x in c:
            amount=x.qty* x.pid.price
            o=Order.objects.create(order_id=orderid,amt=amount,p_id=x.pid,user_id=x.userid)
            o.save()
            #x.delete()

        return redirect("/fetchorder")



def viewbrandcart(request):
    context={}
    b=brandcart.objects.filter(userid=request.user.id)
    context["brandcarts"]=b
    return render(request,"branddetail.html",context)

def addtobrandcart(request,bid):
    context={}
    if request.user.is_authenticated:
        us=User.objects.filter(id=request.user.id)
        b=Brand.objects.filter(id=bid)
        q1=Q(userid=us[0])
        q2=Q(bid=b[0])
        c=Cart.objects.filter(q1 & q2)
         
        n=len(c)
        if n==1:
            context["msg"]="Product already exist in cart"
            return render(request,"branddetail.html",context)
        else:
            cart=Cart.objects.create(userid=us[0],bid=b[0])
            cart.save()
            context["msg"]="Product added in cart successfuly"
            return render(request,"branddetail.html",context)
    else:
        return redirect("/login")



def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile.html')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_I7C0Tt7if7jjRS", "jlibpy1HmtPz4Foe9Sjaky1o"))
    orders=Order.objects.filter(user_id=request.user.id)
    context={}
    context["orders"]=orders
    sum=0
    
    for x in orders:
        sum=sum+x.amt
        orderid=x.order_id
        
        
    

    data = { "amount": sum*100, "currency": "INR", "receipt": orderid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context["payment"]=payment
    return render(request,"pay.html",context)
def fetchorder(request):
    
    orders=Order.objects.filter(user_id=request.user.id)
    context={}
    context["orders"]=orders
    sum=0
    for x in orders:
        sum=sum+x.amt
    context["totalamount"]=sum
    context['n']=len(orders)
    return render(request,"placeorder.html",context)


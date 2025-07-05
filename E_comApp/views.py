from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from E_comApp import forms
from E_comApp import models
from django.contrib import messages
from django.http import JsonResponse
import json
# from reportlab.pdfgen import canvas
# from django.template.loader import get_template
# from .utils import render_to_pdf 
import datetime
from E_comApp.decorators import unauthenticated_users, allowed_users

########### Admin Dashboard ################

@login_required(login_url='login')
@allowed_users(allowed_roles =['admin'])
def index(request):
    customer_count = models.customers.objects.count()
    order_items = models.orderitems.objects.count()
    order = models.orders.objects.filter(complete='True').all()
    tot = 0.0
    order_item_count = 0
    for order_obj in order:
        order_items = order_obj.orderitems_set.all()
        order_items_count = order_obj.orderitems_set.all().count()
        order_item_count = order_item_count + order_items_count
        for order_items_obj in order_items:
            product = models.store.objects.get(id=order_items_obj.store.id)
            tot = tot + float(product.price)
    pending_salse_order = 0
    pending_order = models.orders.objects.filter(complete='False').all()
    for pending_obj in pending_order:
        Pending_sales = pending_obj.orderitems_set.all().count()
        pending_salse_order = pending_salse_order + Pending_sales

    customer = models.customers.objects.all()
    context={'customer_count':customer_count,'order_item_count':order_item_count,'tot':tot,
            'Pending_sales':Pending_sales,'pending_salse_order':pending_salse_order,
            'customer':customer,}
    return render(request,"Template/shopTemp/adminPage/index.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles =['admin'])
def store(request):
    storeForm = forms.storeform(request.FILES)
    if request.method == 'POST':
        storeForm = forms.storeform(request.POST,request.FILES)
        if storeForm.is_valid():
            storeForm.save()
            messages.success(request,"Product Added")
            return redirect('stores')
        else:
            messages.info(request,"Product is not Added")
            return redirect('stores')
    context = {'storeForm':storeForm}
    return render(request,"Template/shopTemp/adminPage/product.html",context)

########## Customers ######

@unauthenticated_users
def register(request):
    form = forms.CreateUserForm()
    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            phoneno = request.POST.get('phone')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            models.customers.objects.create(user=user,name=username,phonenumber=phoneno)
            messages.success(request,'Account was created for '+username)
            return redirect('login')
        else:
            messages.info(request,"Password is incorrect. Please include both letters and numbers. Avoid user name contains Password")
    context={'form':form}
    return render(request,"Template/shopTemp/customer/registernew.html",context)

@unauthenticated_users
def loginPage(request):
    logins = forms.loginform() 

    if request.method == "POST":
        logins = forms.loginform(request.POST)
        if logins.is_valid():
            usernames = logins.cleaned_data['username']
            phonno = logins.cleaned_data['number']
            passwords = logins.cleaned_data['password']
            user = authenticate(request,username = usernames,password = passwords)
            customer = models.customers.objects.filter(phonenumber=phonno).first()
            if user is not None:
                if customer and customer.phonenumber==phonno:
                    login(request,user)
                    return redirect('viewstores')
                else:
                    messages.error(request,"Phone Number Incorrect")
            else:
                messages.error(request,"Username or Password Incorrect")
    context={'login':logins}
    return render(request,"Template/shopTemp/customer/loginnew.html",context)

def logoutPage(request):
    logout(request)
    return redirect('login')
########################################## Without authendication ############################
# def register(request):
#     registerFORM = forms.registerform()
#     if request.method=='POST':
#         registerFORM = forms.registerform(request.POST)
#         if registerFORM.is_valid():
#             registerFORM.save()
#             name = registerFORM.cleaned_data['name']
#             messages.success(request,"Account was created"+" "+name)
#             return redirect('signin')
#         else:
#             return redirect('register')
#     context = {"registform":registerFORM}
#     return render(request,'Template/shopTemp/customer/register.html',context)

# def loginPage(request):
#     if request.method == 'POST':
#         logform = forms.loginform(request.POST)
#         if logform.is_valid():
#             phnumber = logform.cleaned_data['number']
#             fetch_user = models.customers.objects.filter(phonenumber=phnumber).first()
#             if fetch_user and fetch_user.phonenumber == phnumber:
#                 messages.success(request,"Hi"+""+fetch_user.name)
#                 return redirect('viewstores')
#                 print(fetch_user.phonenumber)
#                 print(user)
#             else:
#                 messages.info(request,"Invalid Phone Number")
#                 return redirect('signin')
#     else:
#         logform = forms.loginform()
#         context = {'login_users':logform}
#         return render(request,"Template/shopTemp/customer/login.html",context)
################################################################################################
@login_required(login_url='login')
@allowed_users(allowed_roles =['admin','customer'])
def viewstores(request):
    if request.user.is_authenticated:
        customer = request.user.customers
        order,created = models.orders.objects.get_or_create(customers=customer,complete=False)
        item = order.orderitems_set.all()
        cart_count = order.get_item_count    
    else:
        item = ""
        order = {'get_item_count':0,'get_item_cardtotal':0}
        cart_count = order['get_item_count']

        ## search item in search bar
    if request.method == 'POST':
        if request.user.is_authenticated:
            search_data = request.POST.get('search')
            searchs = models.store.objects.filter(productname = search_data).first()
            cart_count = order.get_item_count
            context = {'searchs':searchs,'cart_count':cart_count}
            return render(request,'Template/shopTemp/customer/store.html',context)  
        else:
            search_data = request.POST.get('search')
            searchs = models.store.objects.filter(productname = search_data).first()
            cart_count = order['get_item_count']  
            context = {'searchs':searchs,'cart_count':cart_count}
            return render(request,'Template/shopTemp/customer/store.html',context)

    stores = models.store.objects.all()
    return render(request,'Template/shopTemp/customer/store.html',{'stores':stores,'cart_count':cart_count})

@login_required(login_url='login')
@allowed_users(allowed_roles =['admin','customer'])
def viewproduct(request,id): 
    if request.user.is_authenticated:
        customer = request.user.customers
        order,created = models.orders.objects.get_or_create(customers=customer,complete=False)
        item = order.orderitems_set.all()
        cart_count = order.get_item_count
    else:
        item = ""
        order = {'get_item_count':0,'get_item_cardtotal':0}
        cart_count = order['get_item_count']

    singleItem = models.store.objects.get(id=id)
    context={'singleItem':singleItem,'cart_count':cart_count}
    return render(request,"Template/shopTemp/customer/viewproduct.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles =['admin','customer'])
def items(request):
    if request.user.is_authenticated:
        customer = request.user.customers
        order,created = models.orders.objects.get_or_create(customers=customer,complete=False)
        item = order.orderitems_set.all()
        cart_count = order.get_item_count
    else:
        item = ""
        order = {'get_item_count':0,'get_item_cardtotal':0}
        cart_count = order['get_item_count']

    context = {'item':item,'order':order,'cart_count':cart_count}
    return render(request,"Template/shopTemp/customer/items.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles =['admin','customer'])
def updateitem(request):
    data = json.loads(request.body)
    productID = data['productId']
    action = data['action']
    # print('productID:',productID)
    # print('action:',action)

    customer = request.user.customers
    order,created = models.orders.objects.get_or_create(customers=customer,complete=False)
    store = models.store.objects.get(id=productID)
    item,created = models.orderitems.objects.get_or_create(orders=order,store=store)

    if action == 'add':
        item.quantity = (item.quantity + 1)
    elif action == 'remove':
        item.quantity = (item.quantity - 1)
    item.save()

    if item.quantity <= 0:
        item.delete()
    return JsonResponse('Item Added', safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles =['admin','customer'])
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customers
        order,created = models.orders.objects.get_or_create(customers=customer,complete=False)
        item = order.orderitems_set.all()
        cart_count = order.get_item_count

        # Address Create and Update 
        if request.method == 'POST':
            street = request.POST.get('street')
            city = request.POST.get('city')
            district = request.POST.get('district')
            state = request.POST.get('state')
            zipcode = request.POST.get('zip')

            customer = request.user.customers
            order, created = models.orders.objects.get_or_create(customers=customer,complete=False)
            ship_count = order.shipsaddress_set.filter(customers=customer).count()
            print(ship_count)
            if ship_count == 0:
                shipping = models.shipsaddress.objects.create(customers=customer,orders=order,street=street,city=city,district=district,state=state,zipcode=zipcode)
                messages.info(request,"Address Save")
            else:
                shipping = models.shipsaddress.objects.filter(customers=customer).update(customers=customer,orders=order,street=street,city=city,district=district,state=state,zipcode=zipcode)
                messages.info(request,"Address Updated")
            shipping = models.shipsaddress.objects.filter(customers=customer).first()
            context = {'item':item,'order':order,'cart_count':cart_count,'shipping':shipping}
            return render(request,"Template/shopTemp/customer/checkout.html",context)
        elif request.method == "GET" and order==order:
            shipping = models.shipsaddress.objects.filter(customers=customer).first()
        else:
            shipping=""
    else:
        item = ""
        order = {'get_item_count':0,'get_item_cardtotal':0}
        cart_count = order['get_item_count']
        shipping=""
    context = {'item':item,'order':order,'cart_count':cart_count,'shipping':shipping}
    return render(request,"Template/shopTemp/customer/checkout.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles =['admin','customer'])
def ordernow(request):
    data = json.loads(request.body)
    order_id = data['order_id']
    action = data['action']
    # print(order_id,action)

    customer = request.user.customers
    order = models.orders.objects.get(customers=customer,complete=False)
    item = order.orderitems_set.all().count()
    if action == 'False' and item != 0:
        customer = request.user.customers
        order_no = (int(order_id) + 1)
        order_update = models.orders.objects.filter(id=order_id,customers=customer).update(complete=True,orderno=order_no)
        data = {'order_no':order_no,'boolean':'True'}
    else:
        # print("Item count is null")
        data = {'cart':'Cart is empty','boolean':'False'}
    return JsonResponse(data,safe=False)
##################################### Reference ###############################################
################ Html To PDF Created############################################################
# def invoice(request, *args, **kwargs):
#     if request.user.is_authenticated:
#         customer = request.user.customers
#         order,created = models.orders.objects.get_or_create(customers=customer,complete=False)
#         item = order.orderitems_set.all()
#         cart_count = order.get_item_count 
#         date = datetime.datetime.now()
#         context = {'item':item,'order':order,'cart_count':cart_count,'date':date}
#         pdf = render_to_pdf("Template/shopTemp/customer/invoice.html",context)
#         res = HttpResponse(pdf, content_type='application/pdf')
#         res['Content-Disposition'] = 'attachment; filename="Invoice.pdf"'
#         return res

###############PDF Created ####################################################################
# def invoice(request):
    # res = HttpResponse(content_type="application/json")
    # res['Content-Disposition'] = 'attachment; filename="Invoice.pdf"'  
    # p = canvas.Canvas(res)  
    # p.setFont("Times-Roman", 20)  
    # p.drawString(100,700,"Hi Faiyas,") 
    # p.drawString(100,650,"order Qty :5") 
    # p.drawString(100,600,"order Total :2000")  
    # p.showPage()  
    # p.save()  
    # return res  
###############################################################################################



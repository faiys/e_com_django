from django.urls import path
from E_comApp import views
urlpatterns = [
    ## Without authendication
    # path('reg/',views.register, name='register'),
    # path('login/',views.loginPage, name='signin'),

################### Admin pages #############
    path('index/',views.index, name='index'),
    path('store/',views.store, name='stores'),
#################################################

    ## Django authendication Customers
    path('register/',views.register, name='register'),
    path('',views.loginPage, name='login'),
    path('logout/',views.logoutPage, name='logout'),

    path('viewstores/',views.viewstores,name="viewstores"),
    path('viewproduct/<int:id>/',views.viewproduct,name="viewproduct"),
    path('items/',views.items,name='items'),
    path('updateitem/',views.updateitem,name='updateitem'),
    path('checkout/',views.checkout,name='checkout'),
    # path('invoice/',views.invoice,name='invoice'),
    path('ordernow/',views.ordernow,name='ordernow'),
]
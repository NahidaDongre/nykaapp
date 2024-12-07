"""
URL configuration for pmproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Nyka import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home),
    path('cart/',views.cart),
    path('Categories/',views.Categories),
    path('about/',views.about),
    path('contact/',views.contact),
    path('register/',views.register),
    path('ulogin/',views.ulogin,name='login'),
    path('logout/',views.ulogout),
    path('catfilter/<cv>/',views.catfilter),
    path('sortbyprice/<sp>/',views.sortbyprice),
    path('filterbyprice/',views.filterbyprice),
    path('productsdetail/<rid>',views.productsdetail),
    path('viewcart/',views.viewcart),
    path('addtocart/<pid>',views.addtocart),
    path('updateqty/<x>/<cid>/',views.updateqty),
    path('branddetail/<bid>/',views.branddetail,name='branddetail'),
    path('brand/',views.brand),
    path('placeorder/',views.placeorder),
    path('fetchorder/',views.fetchorder),
    path('brandcart/',views.brandcart),
    path('removecart/<cid>/',views.removecart),
    path('viewbrandcart/',views.viewbrandcart),
    path('addtobrandcart/<pid>',views.addtobrandcart),
    path('profile/', views.profile, name='profile'),
    path('makepayment/',views.makepayment),
    
    
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

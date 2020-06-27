"""custmgt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('', home_view, name="home"),
    path('home/', home_view, name="home"),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    
    path('products/', product_view, name="products"),
    path('customers/<int:id>', customer_view, name="customers"),
    path('create-order/', create_order, name="create-order"),
    path('update-order/<int:id>', update_order, name="update-order"),
    path('delete-order/<int:id>', delete_order, name="delete-order"),
    # user permissions
    path('user/', user_view, name="user"),
    path('settings/', user_settings_view, name="user-settings"),


    
]

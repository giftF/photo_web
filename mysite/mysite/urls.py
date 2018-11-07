"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import include, url
from photo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.hello),
    url(r'^validate/', views.validate),
    url(r'^add_validate/', views.add_validate),
    url(r'^found/', views.found),
    url(r'^found_result/', views.found_result),
    url(r'^delete_catalog/$', views.delete_catalog),
    url(r'^to_edit_catalog/$', views.to_edit_catalog),
    url(r'^to_add_photo/$', views.to_add_photo),
    url(r'^add_photo/', views.add_photo),
    url(r'^delete_photo/$', views.delete_photo),
    url(r'^show_photo/', views.show_photo),
    url(r'^return_catalog/', views.return_catalog),
    url(r'^logout/', views.logout),
    url(r'^edit_logout/', views.edit_logout),
]
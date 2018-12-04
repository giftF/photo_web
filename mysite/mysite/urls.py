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
from photo import views, mini_background, mini_nose

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
    url(r'^mini/', mini_background.mini_index),
    url(r'^mini_login/', mini_background.mini_login),
    url(r'^mini_find/', mini_background.mini_find),
    url(r'^mini_add_page/', mini_background.mini_add_page),
    url(r'^mini_add/', mini_background.mini_add),
    url(r'^mini_edit_page/$', mini_background.mini_edit_page),
    url(r'^mini_delete/$', mini_background.mini_delete),
    url(r'^mini_setuser/', mini_nose.mini_setuser),
    url(r'^mini_read/', mini_nose.mini_read),
    url(r'^mini_search/', mini_nose.mini_search),
]
"""librarian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from library import views

app_name = 'library'
urlpatterns = [
    path('', views.home),
    path('search/', views.search),
    path('<str:type>/add/', views.add, name='add'),
    path('<str:type>/add/success/', views.add, {'success': True}),
    path('<str:type>/<int:id>/edit/', views.edit),
    path('<str:type>/<int:id>/edit/success', views.edit, {'success': True}),
    path('<str:type>/<int:id>/', views.show),
    path('<str:type>/', views.show_all),
    #path('@me/', views.profile)
    #path('@me/edit', views.profile_edit)
]

"""uid URL Configuration

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
from home import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='Home'),
    path('about/', views.about, name='About'),
    path('forum/', views.forum, name='Forum'),
    path('news/', views.news, name='News'),

    path('header/', views.header, name = 'just_head'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name = 'logout'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('admins/', views.admin_home, name='admin_home'),
    path('admin_header/', views.admin_header, name='admin_header'),
    path('admin_navbar/', views.admin_navbar, name='admin_navbar'),
    path('admin_footer/', views.admin_footer, name='admin_footer'),
    path('admin_latestnews/', views.admin_latestnews, name='admin_latestnews'),
    path('admin_profilepage/', views.admin_profilepage, name='admin_profilepage'),
    path('admin_aboutus/', views.admin_aboutus, name='admin_aboutus'),
    path('admin_registerpage/', views.admin_registerpage, name='admin_registerpage'),
    path('admin_category/', views.admin_category, name='admin_category'),
    path('user_registration/',views.register,name="user_registrarion"),
    path('question_page/',views.question_page,name="question_page"),
    path('read_more/',views.read_more,name="article"),
    path('laws/',views.laws,name="laws"),
    path('survey_q/',views.survey_q,name="surveyq"),
    path('survey_a/',views.survey_a,name="surveya"),
    path('survey/',views.survey,name="survey"),
    path('admin_aggregate/',views.admin_aggregate,name="admin_aggregate"),


]

urlpatterns+=staticfiles_urlpatterns()

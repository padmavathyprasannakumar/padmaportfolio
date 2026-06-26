from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about-me/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('contact-me/', views.contact, name='contact'),
]
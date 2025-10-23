from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_contact, name='contact-submit'),
    path('services/', views.list_services, name='services-list'),
    path('gallery/', views.list_gallery, name='gallery-list'),
    path('process/', views.list_process, name='process-list'),
]

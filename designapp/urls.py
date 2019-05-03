from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("home.html", views.home, name='home'),
    path("vessel_design.html", views.vessel_design, name='vessel_design'),
    path("bibliography.html", views.bibliography, name='bibliography'),
    path("contact.html", views.contact, name='contact'),
    path("vessel_design_results.html", views.vessel_design, name='vessel_design_results')
    ]

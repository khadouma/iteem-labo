from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('analyse/<int:analyse_id>/', views.generate_pdf_analyse, name='generate_pdf_analyse'),
]
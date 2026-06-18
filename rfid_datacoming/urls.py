from django.urls import path
from . import views

urlpatterns = [
    # Route for logging raw scans
    path('api/rfid-log/', views.receive_rfid_drf, name='receive_rfid_drf'),
    
    # Route for verifying tags and logging attendance
    path('api/check-attendance/', views.check_attendance, name='check_attendance'),
]
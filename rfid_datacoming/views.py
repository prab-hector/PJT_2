from django.shortcuts import render
from storage.models import Teammates,AttendanceLog
from django.utils import timezone

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import RFIDLog

@api_view(['POST'])
@permission_classes([AllowAny]) # Allows the ESP32 to connect without authentication
def receive_rfid_drf(request):
    scanned_uid = request.data.get('uid') # DRF automatically parses JSON
    
    if scanned_uid:
        RFIDLog.objects.create(uid=scanned_uid)
        return Response({"status": "Data fetched successfully"}, status=status.HTTP_201_CREATED)
        
    return Response({"error": "No UID provided"}, status=status.HTTP_400_BAD_REQUEST)

    user_exists = Employee.objects.filter(rfid_uid=scanned_uid).exists()
    
@api_view(['POST'])
@permission_classes([AllowAny])
def check_attendance(request):
    # Fetch the scanned UID from the ESP32 payload
    scanned_uid = request.data.get('uid')
    
    if not scanned_uid:
        return Response({"error": "No UID provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 2. Your If-Else Logic using Django DB queries
    # Look for a registered user matching this RFID tag
    user_exists = Teammates.objects.filter(rfid_uid=scanned_uid).exists()
    
    if user_exists:
        # Fetch the user profile data
        user = Teammates.objects.get(rfid_uid=scanned_uid)
        
        # Log their attendance in the database
        AttendanceLog.objects.create(
            employee=user,
            timestamp=timezone.now(),
            status="Present"
        )
        
        print(f"[SUCCESS] Attendance marked for: {user.name}")
        return Response({
            "status": "allowed",
            "message": f"Welcome, {user.name}!"
        }, status=status.HTTP_200_OK)
        
    else:
        # The scanned ID does not match any ID in your storage
        print(f"[REJECTED] Unknown RFID Tag: {scanned_uid}")
        return Response({
            "status": "denied",
            "message": "Access Denied: Unknown Card"
        }, status=status.HTTP_401_UNAUTHORIZED)   
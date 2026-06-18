from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# Model imports
from storage.models import Teammates, AttendanceLog
from .models import RFIDLog


@api_view(['POST'])
@permission_classes([AllowAny])
def receive_rfid_drf(request):
    """
    Logs every raw RFID scan directly into the database.
    """
    scanned_uid = request.data.get('uid')
    
    if scanned_uid:
        RFIDLog.objects.create(uid=scanned_uid)
        return Response({"status": "Data fetched successfully"}, status=status.HTTP_201_CREATED)
        
    return Response({"error": "No UID provided"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_attendance(request):
    """
    Validates the RFID UID, logs attendance if matched, or denies entry.
    """
    scanned_uid = request.data.get('uid')
    
    if not scanned_uid:
        return Response({"error": "No UID provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Optimizing database hit: Attempting to grab the user directly
        user = Teammates.objects.get(rfid_uid=scanned_uid)
        
        # Log attendance record
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
        
    except Teammates.DoesNotExist:
        # Code block triggers if no match is found in the database
        print(f"[REJECTED] Unknown RFID Tag: {scanned_uid}")
        return Response({
            "status": "denied",
            "message": "Access Denied: Unknown Card"
        }, status=status.HTTP_401_UNAUTHORIZED)
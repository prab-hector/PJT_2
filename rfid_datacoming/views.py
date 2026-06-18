from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# Model imports
from storage.models import Teammates, AttendanceLog
from .models import RFIDLog


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])  # Bypasses session cookies verification for hardware clients
def receive_rfid_drf(request):
    """
    Logs every raw RFID scan directly into the database.
    Useful for registering new tags or keeping a raw history trail.
    """
    scanned_uid = request.data.get('uid')
    
    if scanned_uid:
        RFIDLog.objects.create(uid=scanned_uid)
        return Response({"status": "Data fetched successfully"}, status=status.HTTP_201_CREATED)
        
    return Response({"error": "No UID provided"}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])  # Bypasses session cookies verification for hardware clients
def check_attendance(request):
    """
    Validates an incoming ESP32 RFID string against registered Teammates.
    Creates a timestamp log inside AttendanceLog if matching database records exist.
    """
    scanned_uid = request.data.get('uid')
    
    if not scanned_uid:
        return Response({"error": "No UID provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Matches against the 'rfid_num' field from your storage.Teammates model
        user = Teammates.objects.get(rfid_num=scanned_uid)
        
        # Creates an entry tracking back to your uppercase field relation 'Teammates'
        AttendanceLog.objects.create(
            Teammates=user,
            timestamp=timezone.now(),
            status="Present"
        )
        
        print(f"[SUCCESS] Attendance marked for: {user.name}")
        return Response({
            "status": "allowed",
            "message": f"Welcome, {user.name}!"
        }, status=status.HTTP_200_OK)
        
    except Teammates.DoesNotExist:
        print(f"[REJECTED] Unknown RFID Tag: {scanned_uid}")
        return Response({
            "status": "denied",
            "message": "Access Denied: Unknown Card"
        }, status=status.HTTP_401_UNAUTHORIZED)
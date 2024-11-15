# attendance/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Student, Attendance
from .serializers import StudentSerializer, AttendanceSerializer
from django.shortcuts import get_object_or_404

# Student ViewSet
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

# Attendance ViewSet
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(detail=False, methods=['get'], url_path='by-student/(?P<student_id>[^/.]+)')
    def list_by_student(self, request, student_id=None):
        # List attendance records by student ID
        attendance_records = Attendance.objects.filter(student_id=student_id)
        serializer = self.get_serializer(attendance_records, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='mark-attendance')
    def mark_attendance(self, request):
        student_id = request.data.get('student_id')
        date = request.data.get('date')
        status = request.data.get('status')
        
        # Ensure unique attendance record for a student and date
        attendance, created = Attendance.objects.update_or_create(
            student_id=student_id,
            date=date,
            defaults={'status': status}
        )
        serializer = self.get_serializer(attendance)
        return Response(serializer.data, status=status.HTTP_200_OK if created else status.HTTP_202_ACCEPTED)

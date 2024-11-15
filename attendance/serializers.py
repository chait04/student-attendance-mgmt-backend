# attendance/serializers.py

from rest_framework import serializers
from .models import Student, Attendance

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email']

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), source='student')

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_id', 'date', 'status']

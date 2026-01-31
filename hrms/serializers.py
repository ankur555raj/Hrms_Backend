from rest_framework import serializers
from .models import Employee, Attendance


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model"""
    
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'full_name', 'email', 'department', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_employee_id(self, value):
        """Validate employee_id is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Employee ID cannot be empty")
        return value.strip()

    def validate_full_name(self, value):
        """Validate full_name is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Full name cannot be empty")
        return value.strip()

    def validate_department(self, value):
        """Validate department is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Department cannot be empty")
        return value.strip()


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance model"""
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id_display = serializers.CharField(source='employee.employee_id', read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 
            'employee', 
            'employee_name', 
            'employee_id_display',
            'date', 
            'status', 
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'employee_name', 'employee_id_display']

    def validate(self, data):
        """Validate attendance data"""
        employee = data.get('employee')
        date = data.get('date')
        
        # Check for duplicate attendance on update
        if self.instance:
            # Update case
            if Attendance.objects.filter(
                employee=employee, 
                date=date
            ).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError(
                    "Attendance for this employee on this date already exists"
                )
        else:
            # Create case
            if Attendance.objects.filter(employee=employee, date=date).exists():
                raise serializers.ValidationError(
                    "Attendance for this employee on this date already exists"
                )
        
        return data


class AttendanceStatsSerializer(serializers.Serializer):
    """Serializer for attendance statistics"""
    employee_id = serializers.CharField()
    employee_name = serializers.CharField()
    total_present = serializers.IntegerField()
    total_absent = serializers.IntegerField()
    total_days = serializers.IntegerField()

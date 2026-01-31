from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from .models import Employee, Attendance
from .serializers import (
    EmployeeSerializer, 
    AttendanceSerializer,
    AttendanceStatsSerializer
)


@api_view(['GET', 'POST'])
def employee_list(request):
    """
    GET: List all employees
    POST: Create a new employee
    """
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def employee_detail(request, pk):
    """
    DELETE: Delete an employee
    """
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response(
            {'error': 'Employee not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'DELETE':
        employee.delete()
        return Response(
            {'message': 'Employee deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET', 'POST'])
def attendance_list(request):
    """
    GET: List attendance records (with optional employee_id filter)
    POST: Create a new attendance record
    """
    if request.method == 'GET':
        attendances = Attendance.objects.select_related('employee').all()
        
        # Filter by employee_id if provided
        employee_id = request.query_params.get('employee_id', None)
        if employee_id:
            attendances = attendances.filter(employee_id=employee_id)
        
        # Filter by date range if provided
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        
        if start_date:
            attendances = attendances.filter(date__gte=start_date)
        if end_date:
            attendances = attendances.filter(date__lte=end_date)
        
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def attendance_stats(request):
    """
    GET: Get attendance statistics per employee
    """
    employees = Employee.objects.all()
    stats = []
    
    for employee in employees:
        attendances = employee.attendances.all()
        total_present = attendances.filter(status='Present').count()
        total_absent = attendances.filter(status='Absent').count()
        total_days = attendances.count()
        
        stats.append({
            'employee_id': employee.employee_id,
            'employee_name': employee.full_name,
            'total_present': total_present,
            'total_absent': total_absent,
            'total_days': total_days
        })
    
    serializer = AttendanceStatsSerializer(stats, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def dashboard_stats(request):
    """
    GET: Get dashboard statistics
    """
    today = now().date()

    total_employees = Employee.objects.count()
    total_attendance_records = Attendance.objects.count()

    # Today's attendance counts
    today_present = Attendance.objects.filter(
        date=today, status="Present"
    ).count()

    today_absent = Attendance.objects.filter(
        date=today, status="Absent"
    ).count()

    # Get recent attendance
    recent_attendance = Attendance.objects.select_related('employee').all()[:10]
    recent_serializer = AttendanceSerializer(recent_attendance, many=True)
    
    return Response({
        'total_employees': total_employees,
        'total_attendance_records': total_attendance_records,
        'today_present': today_present,
        'today_absent': today_absent,
        'recent_attendance': recent_serializer.data
    })

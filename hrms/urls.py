from django.urls import path
from . import views

urlpatterns = [
    # Employee endpoints
    path('employees/', views.employee_list, name='employee-list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee-detail'),
    
    # Attendance endpoints
    path('attendance/', views.attendance_list, name='attendance-list'),
    path('attendance/stats/', views.attendance_stats, name='attendance-stats'),
    
    # Dashboard endpoints
    path('dashboard/', views.dashboard_stats, name='dashboard-stats'),
]

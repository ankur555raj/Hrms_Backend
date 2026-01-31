"""
URL configuration for HRMS Lite project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('hrms.urls')),
]

# Customize admin site
admin.site.site_header = 'HRMS Lite Administration'
admin.site.site_title = 'HRMS Lite Admin'
admin.site.index_title = 'Welcome to HRMS Lite Administration'

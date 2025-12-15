from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report_item, name='report_item'), 
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('my-reports/', views.my_reports, name='my_reports'),
    path('register/', views.register, name='register'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  
    path('logout/', views.user_logout, name='user_logout'),
    path('delete-item/<int:pk>/', views.delete_item, name='delete_item'),
    path('edit-item/<int:pk>/', views.edit_item, name='edit_item'), # New URL pattern for editing an item 
]

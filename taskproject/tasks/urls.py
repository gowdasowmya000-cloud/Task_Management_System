from django.urls import path
from . import views

urlpatterns = [

    #pages
    path('', views.dashboard_page),
    path('add/', views.add_task_page),
    path('update/<int:id>/', views.update_task_page),
    path('login/', views.login_page),
    path('profile/', views.profile_page),

    # APIs
    path('api/tasks/', views.get_tasks),
    path('api/create/', views.create_task),
    path('api/update/<int:id>/', views.update_task),
    path('api/delete/<int:id>/', views.delete_task),
    path('api/login/', views.login_api),
    path('api/logout/', views.logout_api),
    path('api/send-otp/', views.send_otp),
    path('api/verify-otp/', views.verify_otp),
    path('api/reset-password/', views.reset_password),

]
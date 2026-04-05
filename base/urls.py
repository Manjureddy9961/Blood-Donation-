from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/donor/', views.register_donor, name='register_donor'),
    path('register/hospital/', views.register_hospital, name='register_hospital'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/donor/', views.donor_dashboard, name='donor_dashboard'),
    path('dashboard/hospital/', views.hospital_dashboard, name='hospital_dashboard'),
    path('request/update/<int:request_id>/<str:status>/', views.update_request_status, name='update_request_status'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('gallery/delete/<int:image_id>/', views.delete_image, name='delete_image'),
    path('recommend-donors/', views.recommend_donors_view, name='recommend_donors'),
    path('admin/request/<int:request_id>/complete/', views.mark_donation_completed, name='admin_mark_donation_completed'),
    path('verify-qr/<int:request_id>/', views.verify_qr, name='verify_qr'),
]

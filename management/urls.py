from django.urls import path
from . import views

urlpatterns = [
    # Root Routing
    path('', views.root_redirect, name='root_redirect'),

    # Public & User URLs
    path('plans/', views.PlansView.as_view(), name='plans'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('choose-membership/', views.ChooseMembershipView.as_view(), name='choose_membership'),
    path('client/dashboard/', views.ClientDashboardView.as_view(), name='client_dashboard'),
    
    # Admin URLs
    path('management/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('management/clients/', views.AdminClientListView.as_view(), name='admin_client_list'),
    path('management/clients/<int:pk>/delete/', views.AdminClientDeleteView.as_view(), name='client_delete'),
    
    # Admin Membership Management
    path('management/memberships/new/', views.AdminMembershipCreateView.as_view(), name='membership_new'),
    path('management/memberships/<int:pk>/edit/', views.AdminMembershipUpdateView.as_view(), name='membership_edit'),
    path('management/memberships/<int:pk>/delete/', views.AdminMembershipDeleteView.as_view(), name='membership_delete'),
]

# Django
from django.urls import path

# App
from . import views

urlpatterns = [
    path("placeholder/", views.PlaceholderHome.as_view(), name="supportdesk_placeholder"),
    path('', views.RequestList.as_view(), name='request_list'),
    path('new-request/', views.RequestCreateView.as_view(), name='new_request'),
    path('requests/<str:pk>/', views.RequestDetailView.as_view(), name='request_detail'),
    path('requests/mark-completed/<str:pk>/', views.mark_completed, name='mark_completed'),
    path('requests/reassign/<str:requestID>/<str:agentID>', views.reassign_agent, name='reassign_agent'),
]

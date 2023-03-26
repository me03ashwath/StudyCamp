from django.http import HttpResponse 
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='loginPage'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='registerPage'),

    path('', views.home, name = 'home'),
    path('room/<str:pk>/', views.room, name = 'room'),
    path('user-profile/<str:pk>/', views.userProfile, name='user-profile'),

    path('create-room/', views.createRoom, name = 'create-room'),
    path('update-room/<str:pk>', views.updateRoom, name = 'update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name = 'delete-room'),
    path('room/<str:roomId>/delete-message/<str:pk>', views.deleteMessage, name = 'delete-message'),
    
]
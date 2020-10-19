from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signin/', views.SigninView.as_view(), name="signin"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('friend_request/', views.friend_request, name="friend_request"),
    path('messages/<int:room_id>/', views.messages),
    path('contacts/', views.contacts),
    path('search/<str:search_query>/', views.search),
    path('notifications/', views.notifications),
    path('accept_friend_request/<int:id>/', views.accept_friend_request, name="accept_friend_request"),
    path('reject_friend_request/<int:id>/', views.reject_friend_request, name="reject_friend_request"),
    path('profile/', views.profile),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('delete_profile/', views.delete_profile, name="delete_profile"),
]
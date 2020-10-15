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
]
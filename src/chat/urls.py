from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signin/', views.SigninView.as_view(), name="signin"),
    path('signup/', views.signup, name="signup"),
]
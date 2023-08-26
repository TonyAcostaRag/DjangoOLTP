from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('', views.endpoints),
    path('users/', views.UserList.as_view()),
    path('users/<str:username>', views.UserDetail.as_view()),
    path('users/<str:username>/accounts/', views.account_list),
    path('users/<str:username>/accounts/<str:account_name>', views.AccountDetail.as_view()),
    path('users/<str:username>/accounts/<str:account_name>/cards/', views.card_list),
    path('users/<str:username>/accounts/<str:account_name>/cards/<str:account>', views.CardDetail.as_view())
]

from django.urls import path
from . import views
from . views import  ServicerLogin, ServicerRegister
from .models import Servicer
from .views import  ServicerRegister,BlockServicerView,UnblockServicerView
from .views import MyServicerTokenObtainPairView, ServicerLoginView
from rest_framework_simplejwt.views import (
  
    TokenRefreshView,
)


urlpatterns = [
    path('api/token/', MyServicerTokenObtainPairView.as_view(), name='token_obtain_pair'),  # For sellers (renters)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Add other URL patterns for your views
    path('servicerlogin/', ServicerLoginView.as_view(), name='servicer_login'),
   
    path('servicerlogin/', views.ServicerLogin.as_view()),
    path('servicersignup/', ServicerRegister.as_view()),
    path('block/<int:pk>/', BlockServicerView.as_view(), name='block_Servicer'),
    path('servicer/unblock/<int:servicer_id>/', UnblockServicerView.as_view(), name='unblock_Servicer'),
   
]
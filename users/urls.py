from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('google_login/', Google_login.as_view(), name = 'google_login'),
    path('signup/', Signup.as_view(), name = 'Signup'),
    path('verify/<str:uidb64>/<str:token>/', VerifyUserView.as_view(), name = 'verify-user'),
    path('google_signup/', Google_Signup.as_view(), name = 'google_signup'),
    path('token/', MyTokenObtainPairView.as_view(), name='MyTokenObtainPairView'),
    path('token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
]

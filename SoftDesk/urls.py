from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('api/v1/signup/', include('rest_auth.registration.urls'), name='signup'),
    path('api/v1/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/v1/login/refresh', TokenRefreshView.as_view(), name='refresh'),
]

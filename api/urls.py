from django.urls import path
from .views import AllProjectsAPIView, ProjectAPIView

urlpatterns = [
    path('projects/', AllProjectsAPIView.as_view(), name='user_projects'),
    path('projects/<int:id_project>/', ProjectAPIView.as_view(), name='user_projects'),
]

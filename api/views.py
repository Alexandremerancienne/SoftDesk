from rest_framework import viewsets
from rest_framework.decorators import action

from todos.models import Project
from rest_framework import permissions
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=['get'])
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(author=user)
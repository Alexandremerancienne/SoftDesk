from rest_framework import generics

from todos.models import Project
from .serializers import ProjectSerializer


class AllProjectsAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(author=user)


class ProjectAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        id_project = self.kwargs['id_project']
        return Project.objects.filter(id=id_project)

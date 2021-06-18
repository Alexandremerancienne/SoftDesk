from rest_framework import viewsets
from rest_framework.decorators import action

from todos.models import Project, Issue, Comment
from rest_framework import permissions
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True)
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(author=user)


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()

    @action(detail=True)
    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    @action(detail=True)
    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issue_pk'])


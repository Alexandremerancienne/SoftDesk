from rest_framework import viewsets
from rest_framework.decorators import action

from todos.models import Project, Issue, Comment, Contributor
from rest_framework import permissions
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer, ContributorSerializer
from .permissions import IsProjectContributorOrAuthor, IsIssueAuthorOrContributorReadOnly
from .permissions import IsCommentAuthorOrContributorReadOnly


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsProjectContributorOrAuthor,)
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    @action(detail=True)
    def get_queryset(self):
        user = self.request.user
        return Contributor.objects.filter(user=user)


class ContributorViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()

    @action(detail=True)
    def get_queryset(self):
        return Contributor.objects.filter(project=self.kwargs['project_pk'])


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsIssueAuthorOrContributorReadOnly,)
    serializer_class = IssueSerializer
    queryset = Issue.objects.all()

    @action(detail=True)
    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsCommentAuthorOrContributorReadOnly,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    @action(detail=True)
    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issue_pk'])


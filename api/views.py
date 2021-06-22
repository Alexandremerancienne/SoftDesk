from rest_framework import viewsets
from rest_framework.decorators import action

from todos.models import Issue, Comment, Contributor, Project
from .serializers import IssueSerializer, CommentSerializer, ContributorSerializer, ProjectSerializer
from .permissions import IsProjectAuthorOrContributorReadOnly, IsIssueAuthorOrContributorReadOnly, IsProjectAuthor
from .permissions import IsCommentAuthorOrContributorReadOnly


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsProjectAuthorOrContributorReadOnly,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True)
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(contributor__user__id=user.id)


class ContributorViewSet(viewsets.ModelViewSet):
    permission_classes = (IsProjectAuthor,)
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


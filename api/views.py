from rest_framework.response import Response
from rest_framework import viewsets, status

from accounts.models import Users
from todos.models import Issue, Comment, Contributor, Project
from .serializers import (
    IssueSerializer,
    CommentSerializer,
    ContributorSerializer,
    ProjectSerializer,
)
from .permissions import (
    IsProjectAuthorOrContributorReadOnly,
    IsIssueAuthorOrContributorReadOnly,
    IsProjectAuthor,
    IsCommentAuthorOrContributorReadOnly,
)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (IsProjectAuthorOrContributorReadOnly,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request):
        user = self.request.user
        queryset = Project.objects.filter(contributor__user=user)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_project = serializer.save()
        author = Contributor.objects.create(
            user=request.user, project=new_project, role="author"
        )
        author.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContributorViewSet(viewsets.ModelViewSet):
    permission_classes = (IsProjectAuthor,)
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

    def list(self, request, project_pk=None):
        queryset = Contributor.objects.filter(
            project=project_pk, project__contributor__user=request.user
        )
        if queryset.count() == 0:
            return Response({'detail': 'You are not a member of this project'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = ContributorSerializer(queryset, many=True)
            return Response(serializer.data)

    def create(self, request, project_pk=None):
        contributors = Contributor.objects.filter(
            project=project_pk, project__contributor__user=request.user
        )
        if contributors.count() == 0:
            return Response({'detail': 'You are not a member of this project'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            user_data = request.data['user']
            if user_data:
                try:
                    Users.objects.get(id=user_data)
                except:
                    return Response({'detail': 'Invalid request: enter valid user ID'},
                                    status=status.HTTP_404_NOT_FOUND)
                id_list = [str(contributor.user.id) for contributor in contributors]
                if id_list.count(user_data) != 0:
                    return Response({'detail': 'Invalid request: '
                                               'user already registered as a contributor'},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer = ContributorSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(project_id=int(project_pk))
                    return Response(serializer.data, status=status.HTTP_201_CREATED)


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsIssueAuthorOrContributorReadOnly,)
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def list(self, request, project_pk=None):
        user = self.request.user
        queryset = Issue.objects.filter(
            project_id=project_pk, project__contributor__user=user
        )
        if queryset.count() == 0:
            return Response({'detail': 'You are not a member of this project'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = IssueSerializer(queryset, many=True)
            return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsCommentAuthorOrContributorReadOnly,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def list(self, request, project_pk=None, issue_pk=None):
        user = self.request.user
        queryset = Comment.objects.filter(
            issue_id=issue_pk,
            issue__project_id=project_pk,
            issue__project__contributor__user=user
        )
        if queryset.count() == 0:
            return Response({'detail': 'You are not a member of this project'},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = CommentSerializer(queryset, many=True)
            return Response(serializer.data)

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
from .exceptions import (
    InvalidProjectNumber,
    InvalidIssueNumber,
    InvalidCommentNumber,
    ProjectNotFound,
    ContributorNotFound,
    AssigneeNotFound,
    IssueNotFound,
    CommentNotFound,
    NotContributor,
    UserNotFound,
    AlreadyContributor,
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

    def retrieve(self, request, pk=None):
        user = request.user
        queryset = Project.objects.filter(id=pk, contributor__user=user)
        if queryset.count() == 0:
            raise ProjectNotFound()
        project = queryset.first()
        serializer = ProjectSerializer(project)
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
        try:
            int(project_pk)
        except ValueError:
            raise InvalidProjectNumber()
        queryset = Contributor.objects.filter(
            project_id=project_pk, project__contributor__user=request.user
        )
        if queryset.count() == 0:
            raise ProjectNotFound()
        else:
            serializer = ContributorSerializer(queryset, many=True)
            return Response(serializer.data)

    def create(self, request, project_pk=None):
        try:
            int(project_pk)
        except ValueError:
            raise InvalidProjectNumber()
        projects = Project.objects.filter(id=project_pk)
        if projects.count() == 0:
            raise ProjectNotFound()
        contributors = Contributor.objects.filter(
            project=project_pk, project__contributor__user=request.user
        )
        if contributors.count() == 0:
            raise NotContributor()
        else:
            try:
                user_data = request.data["user"]
                Users.objects.get(id=user_data)
            except Exception:
                raise UserNotFound()
            id_list = [str(contributor.user.id)
                       for contributor in contributors]

            if id_list.count(user_data) != 0:
                raise AlreadyContributor()
            else:
                request_copy = request.data.copy()
                request_copy["role"] = "contributor"
                serializer = ContributorSerializer(data=request_copy)
                serializer.is_valid(raise_exception=True)
                serializer.save(project_id=int(project_pk))
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

    def destroy(self, request, project_pk=None, pk=None):
        try:
            int(project_pk)
        except ValueError:
            raise InvalidProjectNumber()
        try:
            int(pk)
        except ValueError:
            raise InvalidIssueNumber()
        try:
            contributor = Contributor.objects.get(project_id=project_pk,
                                                  user_id=pk)
            self.perform_destroy(contributor)
        except Exception:
            raise ContributorNotFound()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = (IsIssueAuthorOrContributorReadOnly,)
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def list(self, request, project_pk=None):
        try:
            int(project_pk)
        except ValueError:
            raise InvalidProjectNumber()
        user = self.request.user
        try:
            Project.objects.get(id=project_pk, contributor__user=user)
        except Exception:
            raise ProjectNotFound()
        queryset = Issue.objects.filter(
            project_id=project_pk,
        )
        serializer = IssueSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, project_pk=None, pk=None):
        user = request.user
        queryset = Issue.objects.filter(project_id=project_pk,
                                        id=pk,
                                        project__contributor__user=user)
        if queryset.count() == 0:
            raise IssueNotFound()
        project = queryset.first()
        serializer = IssueSerializer(project)
        return Response(serializer.data)

    def create(self, request, project_pk=None):
        try:
            int(project_pk)
        except ValueError:
            raise InvalidProjectNumber()
        projects = Project.objects.filter(id=project_pk)
        if projects.count() == 0:
            raise ProjectNotFound()
        contributors = Contributor.objects.filter(
            project=project_pk, project__contributor__user=request.user
        )
        if contributors.count() == 0:
            raise NotContributor()
        else:
            try:
                user_data = request.data["assignee"]
                Users.objects.get(id=user_data)
            except Exception:
                raise AssigneeNotFound()
            id_list = [str(contributor.user.id)
                       for contributor in contributors]

            if id_list.count(user_data) == 0:
                raise AssigneeNotFound()
            else:
                request_copy = request.data.copy()
                request_copy["author"] = request.user.id
                request_copy["project"] = project_pk
                serializer = IssueSerializer(data=request_copy)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)

    def update(self, request, project_pk=None, pk=None, **kwargs):
        user = self.request.user
        try:
            int(project_pk)
        except ValueError:
            raise InvalidProjectNumber()
        try:
            int(pk)
        except ValueError:
            raise InvalidIssueNumber()
        try:
            Project.objects.get(id=project_pk, contributor__user=user)
        except Exception:
            raise NotContributor()
        try:
            Issue.objects.get(project_id=project_pk, id=pk)
        except Exception:
            raise IssueNotFound()

        request_copy = request.data.copy()
        request_copy["author"] = request.user.id
        request_copy["project"] = project_pk

        try:
            user_data = request.data["assignee"]
            Users.objects.get(id=user_data)
        except Exception:
            raise AssigneeNotFound()
        contributors = Contributor.objects.filter(
            project=project_pk, project__contributor__user=request.user
        )
        id_list = [str(contributor.user.id)
                   for contributor in contributors]

        if id_list.count(user_data) == 0:
            raise AssigneeNotFound()
        else:
            issue = Issue.objects.get(project_id=project_pk, id=pk)
            self.check_object_permissions(request, issue)
            serializer = IssueSerializer(issue, data=request_copy)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

    def partial_update(self, request, project_pk=None,
                       pk=None, **kwargs):

        user = self.request.user
        try:
            int(project_pk)
        except ValueError:
            raise InvalidProjectNumber()
        try:
            Project.objects.get(id=project_pk, contributor__user=user)
        except Exception:
            raise NotContributor()
        try:
            Issue.objects.get(project_id=project_pk, id=pk)
        except Exception:
            raise IssueNotFound()

        issue = Issue.objects.get(project_id=project_pk, id=pk)
        request_copy = request.data.copy()
        request_copy["author"] = request.user.id
        request_copy["project"] = int(project_pk)

        if not any(
            key in request.data.keys()
            for key in ["assignee", "description", "title",
                        "tag", "priority", "status"]
        ):
            serializer = IssueSerializer(issue)
            return Response(serializer.data)

        for key in request.data.keys():
            if key == "assignee":
                try:
                    user_data = request.data["assignee"]
                    Users.objects.get(id=user_data)
                except Exception:
                    raise AssigneeNotFound()
                contributors = Contributor.objects.filter(
                    project=project_pk,
                    project__contributor__user=request.user
                )
                id_list = [str(contributor.user.id)
                           for contributor in contributors]

                if id_list.count(user_data) == 0:
                    raise AssigneeNotFound()
            else:

                request_copy["assignee"] = issue.assignee.id

                description = "description"
                if description not in request.data.keys():
                    request_copy["description"] = issue.description

                title = "title"
                if title not in request.data.keys():
                    request_copy["title"] = issue.title

                self.check_object_permissions(request, issue)
                serializer = IssueSerializer(issue, data=request_copy)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsCommentAuthorOrContributorReadOnly,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def list(self, request, project_pk=None, issue_pk=None):
        try:
            int(project_pk)
        except ValueError:
            raise InvalidProjectNumber()
        try:
            int(issue_pk)
        except ValueError:
            raise InvalidIssueNumber()

        user = self.request.user
        try:
            Project.objects.get(id=project_pk, contributor__user=user)
        except Exception:
            raise NotContributor()
        try:
            Issue.objects.get(project_id=project_pk, id=issue_pk)
        except Exception:
            raise IssueNotFound()
        queryset = Comment.objects.filter(
            issue_id=issue_pk,
            issue__project_id=project_pk,
            issue__project__contributor__user=user,
        )
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, project_pk=None,
                 issue_pk=None, pk=None):
        user = request.user
        queryset = \
            Comment.objects.filter(issue__project_id=project_pk,
                                   issue_id=issue_pk,
                                   id=pk,
                                   issue__project__contributor__user=user)
        if queryset.count() == 0:
            raise CommentNotFound()
        project = queryset.first()
        serializer = CommentSerializer(project)
        return Response(serializer.data)

    def create(self, request, project_pk=None, issue_pk=None):
        try:
            int(project_pk)
        except ValueError:
            raise InvalidProjectNumber()
        try:
            int(issue_pk)
        except ValueError:
            raise InvalidIssueNumber()

        projects = Project.objects.filter(id=project_pk)
        if projects.count() == 0:
            raise ProjectNotFound()

        issues = Issue.objects.filter(project_id=project_pk)
        if issues.count() == 0:
            raise IssueNotFound()

        contributors = Contributor.objects.filter(
            project=project_pk, project__contributor__user=request.user
        )
        if contributors.count() == 0:
            raise NotContributor()
        else:
            request_copy = request.data.copy()
            request_copy["author"] = request.user.id
            request_copy["project"] = project_pk
            request_copy["issue"] = issue_pk
            serializer = CommentSerializer(data=request_copy)
            serializer.is_valid(raise_exception=True)
            serializer.save(issue_id=int(issue_pk))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, project_pk=None,
               issue_pk=None, pk=None, **kwargs):
        user = self.request.user
        try:
            int(project_pk)
        except ValueError:
            raise InvalidProjectNumber()
        try:
            int(issue_pk)
        except ValueError:
            raise InvalidIssueNumber()
        try:
            int(pk)
        except ValueError:
            raise InvalidCommentNumber()
        try:
            Project.objects.get(id=project_pk, contributor__user=user)
        except Exception:
            raise NotContributor()
        try:
            Issue.objects.get(project_id=project_pk, id=pk)
        except Exception:
            raise IssueNotFound()
        try:
            Comment.objects.get(issue__project_id=project_pk,
                                issue_id=pk, id=pk)
        except Exception:
            raise CommentNotFound()
        else:
            request_copy = request.data.copy()
            request_copy["author"] = request.user.id

            comment = Comment.objects.get(
                issue__project_id=project_pk, issue_id=pk, id=pk
            )
            self.check_object_permissions(request, comment)
            serializer = CommentSerializer(comment, data=request_copy)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

    def partial_update(self, request, project_pk=None,
                       issue_pk=None, pk=None, **kwargs):

        user = self.request.user
        try:
            int(project_pk)
        except ValueError:
            raise InvalidProjectNumber()
        try:
            Project.objects.get(id=project_pk, contributor__user=user)
        except Exception:
            raise NotContributor()
        try:
            Issue.objects.get(project_id=project_pk, id=pk)
        except Exception:
            raise IssueNotFound()
        try:
            int(pk)
        except ValueError:
            raise InvalidCommentNumber()

        comment = Comment.objects.get(issue__project_id=project_pk,
                                      issue_id=issue_pk,
                                      id=pk)
        request_copy = request.data.copy()

        description = "description"
        if description not in request.data.keys():
            request_copy["description"] = comment.description
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

        request_copy["author"] = request.user.id
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request_copy)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

from rest_framework import permissions


class IsProjectAuthorOrContributorReadOnly(permissions.BasePermission):
    message = "You are not the author of this project"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        contributors = obj.contributor_set.all()
        contributors_list = [
            contributor
            for contributor in contributors
            if contributor.user.username == str(request.user)
            and contributor.role == "author"
        ]
        return True if len(contributors_list) != 0 else False


class IsProjectAuthor(permissions.BasePermission):
    message = "You are not the author of this project"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        project = obj.project
        contributors = project.contributor_set.all()
        author_id = [contributor.id for contributor in contributors
                  if contributor.role == 'author']
        print(obj.id)
        print(author_id)
        #return True if obj.id in author_id else False


class IsObjectAuthorOrContributorReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return True if obj.author == request.user else False


class IsIssueAuthorOrContributorReadOnly(IsObjectAuthorOrContributorReadOnly):
    message = "You are not the author of this issue"


class IsCommentAuthorOrContributorReadOnly(IsObjectAuthorOrContributorReadOnly):
    message = "You are not the author of this comment"

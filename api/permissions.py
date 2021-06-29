from rest_framework import permissions


class IsProjectAuthorOrContributorReadOnly(permissions.BasePermission):
    message = (
        "Missing credentials: "
        "You need author status to update-patch-delete this project"
    )

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
    message = "Missing credentials: " \
              "You need author status to add-remove a user"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(obj)
        project = obj.project
        contributors = project.contributor_set.all()
        author_id = [
            contributor.user.id
            for contributor in contributors
            if contributor.role == "author"
        ]
        return True if request.user.id in author_id else False


class IsAuthorOrContributorReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return True if obj.author == request.user else False


class IsIssueAuthorOrContributorReadOnly(IsAuthorOrContributorReadOnly):
    message = (
        "Missing credentials: "
        "You need author status to update-patch-delete this issue"
    )


class IsCommentAuthorOrContributorReadOnly(IsAuthorOrContributorReadOnly):
    message = (
        "Missing credentials: "
        "You need author status to update-patch-delete this comment"
    )

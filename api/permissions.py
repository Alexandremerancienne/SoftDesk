from rest_framework import permissions


class IsProjectContributorOrAuthor(permissions.BasePermission):
    message = 'You are not the author of this project'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS \
                and obj.contributor_set in ['contributor', 'author']:
            return True
        return True if obj.author == request.user else False


class IsIssueAuthorOrContributorReadOnly(permissions.BasePermission):
    message = 'You are not the author of this issue'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS \
                and (obj.author == request.user or obj.assignee == request.user):
            return True
        return True if obj.author == request.user else False


class IsCommentAuthorOrContributorReadOnly(permissions.BasePermission):
    message = 'You are not the author of this comment'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS \
                and (obj.issue.author == request.user or obj.issue.assignee == request.user):
            return True
        return True if obj.author == request.user else False


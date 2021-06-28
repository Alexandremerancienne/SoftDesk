from rest_framework.exceptions import APIException


class InvalidProjectNumber(APIException):
    status_code = 400
    default_detail = "Enter valid Project number"
    default_code = "invalid_project_number"


class InvalidIssueNumber(APIException):
    status_code = 400
    default_detail = "Enter valid Issue number"
    default_code = "invalid_issue_number"


class InvalidCommentNumber(APIException):
    status_code = 400
    default_detail = "Enter valid Comment number"
    default_code = "invalid_comment_number"


class ProjectNotFound(APIException):
    status_code = 404
    default_detail = "Project not found"
    default_code = "project_not_found"


class ContributorNotFound(APIException):
    status_code = 404
    default_detail = "Contributor not found"
    default_code = "contributor_not_found"


class UserNotFound(APIException):
    status_code = 404
    default_detail = "User ID not found"
    default_code = "user_not_found"


class AssigneeNotFound(APIException):
    status_code = 404
    default_detail = "Assignee not found"
    default_code = "assignee_not_found"


class IssueNotFound(APIException):
    status_code = 404
    default_detail = "Issue not found"
    default_code = "issue_not_found"


class CommentNotFound(APIException):
    status_code = 404
    default_detail = "Comment not found"
    default_code = "comment_not_found"


class NotContributor(APIException):
    status_code = 404
    default_detail = "You are not a Contributor " \
                     "to this Project"
    default_code = "not_contributor_to_project"


class AlreadyContributor(APIException):
    status_code = 404
    default_detail = "User already registered " \
                     "as a Contributor"
    default_code = "not_contributor_to_project"

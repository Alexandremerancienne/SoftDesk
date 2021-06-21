from django.conf.urls import url
from django.urls import include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from api.views import ProjectViewSet, IssueViewSet, CommentViewSet, ContributorViewSet

router = SimpleRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'issues', IssueViewSet, basename='issues')

contributors_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
contributors_router.register(r'users', ContributorViewSet, basename='users')

issues_router = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(projects_router.urls)),
    url(r'^', include(contributors_router.urls)),
    url(r'^', include(issues_router.urls)),
]
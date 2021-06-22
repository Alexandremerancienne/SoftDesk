from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    path('signup/', include('rest_auth.registration.urls'), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/refresh', TokenRefreshView.as_view(), name='refresh'),
    url(r'^', include(router.urls)),
    url(r'^', include(projects_router.urls)),
    url(r'^', include(contributors_router.urls)),
    url(r'^', include(issues_router.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CompanyViewSet, PackageViewSet, UserRoleViewSet, UserPermissionsView, UserProfileViewSet, \
    NoticeViewSet, BranchViewSet, AdminSelfSignUp

router = DefaultRouter()
router.register(r'users', UserViewSet) 
router.register(r'companies', CompanyViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'user-roles', UserRoleViewSet)
router.register(r'user-profile', UserProfileViewSet)
router.register(r'notices', NoticeViewSet)
router.register(r'branches', BranchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user-permissions/', UserPermissionsView.as_view(), name="user-permissions"),
    path('self-signup/', AdminSelfSignUp.as_view(), name="self-signup"),
]
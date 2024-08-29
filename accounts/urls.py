from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CompanyViewSet, PackageViewSet, UserRoleViewSet, UserPermissionsView, UserProfileViewSet, \
    NoticeViewSet, BranchViewSet, AdminSelfSignUp, FormEnquiryViewSet, SupportTicketViewSet, ModuleViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet) 
router.register(r'companies', CompanyViewSet)
router.register(r'packages', PackageViewSet)
router.register(r'user-roles', UserRoleViewSet)
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'notices', NoticeViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'form-enquiries', FormEnquiryViewSet)
router.register(r'support-tickets', SupportTicketViewSet)
router.register(r'modules', ModuleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user-permissions/', UserPermissionsView.as_view(), name="user-permissions"),
    path('self-signup/', AdminSelfSignUp.as_view(), name="self-signup"),
]
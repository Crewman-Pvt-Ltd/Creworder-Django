from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CompanyViewSet, PackageViewSet, UserRoleViewSet, UserPermissionsView, \
    UserProfileViewSet, \
    NoticeViewSet, BranchViewSet, AdminSelfSignUp, FormEnquiryViewSet, SupportTicketViewSet, ModuleViewSet, \
    GetSpecificUsers, \
    GetNoticesForUser, DepartmentViewSet, DesignationViewSet, LeaveViewSet, HolidayViewSet, AwardViewSet, \
    AppreciationViewSet, ShiftViewSet, AttendanceViewSet, Testing, GetUsernameSuggestions, AttendanceView, \
    IPRestrictedLoginView

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
router.register(r'departments', DepartmentViewSet)
router.register(r'designations', DesignationViewSet)
router.register(r'leaves', LeaveViewSet)
router.register(r'holidays', HolidayViewSet)
router.register(r'awards', AwardViewSet)
router.register(r'appreciations', AppreciationViewSet)
router.register(r'shifts', ShiftViewSet)
router.register(r'attendances', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('login/', IPRestrictedLoginView.as_view(), name='login'),
    path('user-permissions/', UserPermissionsView.as_view(), name="user-permissions"),
    path('self-signup/', AdminSelfSignUp.as_view(), name="self-signup"),
    path('specific-users/', GetSpecificUsers.as_view(), name="specific-users"),
    path('user-notices/', GetNoticesForUser.as_view(), name="user-notices"),
    path('username-suggestions/', GetUsernameSuggestions.as_view(), name="username-suggestions"),
    path('get-attendance/', AttendanceView.as_view(), name='get-attendance'),
    path('testing/', Testing.as_view(), name="testing")
]

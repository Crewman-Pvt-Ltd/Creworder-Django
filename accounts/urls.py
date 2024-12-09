from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AssignRole,AgentListByManagerAPIView, AgentListByTeamleadAPIView, ManagerViewSet, TeamleadViewSet, UserViewSet, CompanyViewSet, PackageViewSet, UserPermissionsView, \
    UserProfileViewSet, \
    NoticeViewSet, BranchViewSet, AdminSelfSignUp, FormEnquiryViewSet, SupportTicketViewSet, ModuleViewSet, \
    GetSpecificUsers, \
    GetNoticesForUser, DepartmentViewSet, DesignationViewSet, LeaveViewSet, HolidayViewSet, AwardViewSet, \
    AppreciationViewSet, ShiftViewSet, AttendanceViewSet, Testing, GetUsernameSuggestions, AttendanceView, \
    IPRestrictedLoginView,ShiftRosterViewSet,GetPackageModule,CustomAuthGroupViewSet,UserGroupViewSet,\
    GroupPermissionViewSet,PermmisionViewSet,FetchPermissionView,PickUpPointView,TargetView,AdminBankDetailsViewSet,\
    AddAllowIpViewSet,QcViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'packages', PackageViewSet)
# router.register(r'user-roles', UserRoleViewSet)
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
router.register(r'shiftroster', ShiftRosterViewSet, basename='shiftroster')
router.register(r'attendances', AttendanceViewSet)
router.register(r'get-module', GetPackageModule,basename='get-module')
router.register(r'auth-role-group',CustomAuthGroupViewSet,basename='auth-role')
router.register(r'user-group', UserGroupViewSet, basename='user-group')
router.register(r'group-permissions', GroupPermissionViewSet, basename='group-permissions')
router.register(r'pick-up-point', PickUpPointView, basename='pickup-point')
router.register(r'user-target', TargetView, basename='user-target')
router.register(r'admin-bank-details', AdminBankDetailsViewSet, basename='admin-bank-details')
router.register(r'add-ip-forlogin', AddAllowIpViewSet, basename='add-ip-forlogin')
router.register(r'qc',QcViewSet,basename='qc')
# router.register(r'assign-role',AssignRole,basename='assign-role')
urlpatterns = [
    path('', include(router.urls)),
    path('user-permissions/', UserPermissionsView.as_view(), name="user-permissions"),
    path('self-signup/', AdminSelfSignUp.as_view(), name="self-signup"),
    path('specific-users/', GetSpecificUsers.as_view(), name="specific-users"),
    path('user-notices/', GetNoticesForUser.as_view(), name="user-notices"),
    path('username-suggestions/', GetUsernameSuggestions.as_view(), name="username-suggestions"),
    path('get-attendance/', AttendanceView.as_view(), name='get-attendance'),
    path('get-permission-ids/', FetchPermissionView.as_view(), name='fetch-permissions'),
    path('testing/', Testing.as_view(), name="testing"),
    #path('update-agent-teamlead-manager/',UpdateTeamleadManagerAPIView.as_view(),name ='update-teamlead-manager'),
    # get manager and teamlead under all agent
    path('assign-role/', AssignRole.as_view(), name='assign-role'),
    path('agents/by_manager/', AgentListByManagerAPIView.as_view(), name='agent-list-by-manager'),
    path('agents/by_teamlead/', AgentListByTeamleadAPIView.as_view(), name='agent-list-by-teamlead'),
    path('teamleads/', TeamleadViewSet.as_view(), name='get_all_teamleads'),
    path('managers/', ManagerViewSet.as_view(), name='get_all_managers'),

]

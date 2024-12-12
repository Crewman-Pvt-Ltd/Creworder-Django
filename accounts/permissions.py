import pdb
from rest_framework.permissions import BasePermission
from guardian.shortcuts import get_objects_for_user


class CanChangeCompanyStatusPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        pdb.set_trace()
        return request.user.has_perm('accounts.can_change_company_status')
    
class CanLeaveApproveAndDisapprove(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('accounts.can_approve_disapprove_leave')



class IsAdminOrSuperAdmin(BasePermission):
    """
    Custom permission to allow only admin or superadmin to create, update, or delete departments.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Check for user type (admin or superadmin)
        if request.user.profile.user_type == 'superadmin' or request.user.profile.user_type == 'admin':
            return True
        return False
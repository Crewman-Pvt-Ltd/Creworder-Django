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

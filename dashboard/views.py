from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order_Table,OrderDetail,Customer_State
from orders.serializers import OrderDetailSerializer,OrderTableSerializer
from accounts.models import UserProfile,UserTargetsDelails,User
from accounts.serializers import UserProfileSerializer,UserSerializer
from .serializers import UserDetailForDashboard,OrderSerializerDashboard
from django.db.models import Count, OuterRef, Subquery,Sum
from utils.custom_logger import setup_logging
from django.utils import timezone
from django.db.models import Q
from django.db.models import Count
import pdb
import time
import traceback
from datetime import datetime
import logging
logger = logging.getLogger(__name__)
setup_logging(log_file='logs/dashboard_view.log', log_level=logging.WARNING)
class GetUserDashboardtiles(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        start_datetime = datetime(2024, 1, 1, 0, 0)
        end_datetime = datetime(2024, 10, 22, 23, 59)
        agent_ids = UserProfile.objects.filter(manager=request.user.id).values_list('user', flat=True)
        user_ids_for_manager = UserProfile.objects.filter(Q(teamlead__in=agent_ids) | Q(user=request.user.id)).values_list('user', flat=True)
        user_ids_for_manager = set(user_ids_for_manager) | set(agent_ids)
        user_ids_for_manager = list(user_ids_for_manager)
        
        user_ids_for_teamlead = list(UserProfile.objects.filter(teamlead=request.user.id).values_list('user', flat=True))
        user_ids_for_teamlead.append(request.user.id)
        tiles_count = {}
        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_running_tile") 
            or request.user.has_perm("dashboard.can_view_manager_dashboard_running_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_running_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_running_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_running_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_all_dashboard_running_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_running_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_running_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["running_tile_count"] = orders_count
        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_Pending_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_Pending_tile")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_Pending_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_Pending_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_Pending_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=1,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_all_dashboard_Pending_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=1,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_Pending_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=1,
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_Pending_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    order_status=1,
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["pending_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_all_dashboard_repeat_order_tile")
            or request.user.has_perm("dashboard.can_view_own_dashboard_repeat_order_tile")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_repeat_order_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_repeat_order_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_repeat_order_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    repeat_order=1,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_all_dashboard_repeat_order_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    repeat_order=1,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_repeat_order_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    repeat_order=1,
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_repeat_order_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    repeat_order=1,
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["repeat_tile_count"] = orders_count
        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_rejected_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_rejected_tile")
            or request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_rejected_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_manager_dashboard_rejected_tile"
            )
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_rejected_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=3,
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_all_dashboard_rejected_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,                    
                    order_status=3,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_rejected_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    order_status=3,
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_rejected_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=3,
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["rejected_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_in_transit_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_in_transit_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_in_transit_tile")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_in_transit_tile")
        ):
            if request.user.has_perm("dashboard.can_view_all_dashboard_in_transit_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    company=request.user.profile.company,
                    order_status=6,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_all_dashboard_in_transit_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=6,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_in_transit_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    order_status=6,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_in_transit_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=6,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["in-transit_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_accepted_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_accepted_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_accepted_tile")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_accepted_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_accepted_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=2,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm("dashboard.can_view_all_dashboard_accepted_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=2,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_accepted_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,                 
                    order_status=2,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_accepted_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=2,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["accepted_tile_count"] = orders_count
            
        if (
            request.user.has_perm("dashboard.can_view_all_dashboard_no_response_tile")
            or request.user.has_perm("dashboard.can_view_own_dashboard_no_response_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_no_response_tile")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_no_response_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_no_response_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=4,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_all_dashboard_no_response_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=4,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_no_response_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    order_status=4,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_no_response_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=4,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["no_response_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_future_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_future_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_future_tile")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_future_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_future_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=5,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm("dashboard.can_view_all_dashboard_future_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=5,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_future_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    order_status=5,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_future_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=5,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["future_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_delivered_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_delivered_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_delivered_tile")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_delivered_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_delivered_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=7,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_all_dashboard_delivered_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=7,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_delivered_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    order_status=7,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_delivered_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=7,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["delivered_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_in_transit_rto")
            or request.user.has_perm("dashboard.can_view_all_dashboard_in_transit_rto")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_in_transit_rto")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_in_transit_rto")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_delivered_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=8,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_all_dashboard_in_transit_rto"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=8,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_in_transit_rto"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    order_status=8,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_in_transit_rto"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=8,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["in_transit_rto_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_all_dashboard_rto")
            or request.user.has_perm("dashboard.can_view_own_dashboard_rto")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_rto")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_rto")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_rto"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=9,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_all_dashboard_rto"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=9,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_rto"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    order_status=9,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_rto"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=9,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["rto_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_non_serviceable_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_non_serviceable_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_non_serviceable_tile")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_non_serviceable_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_non_serviceable_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=10,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_all_dashboard_non_serviceable_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=10,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_rto"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    order_status=10,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_rto"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=10,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["non_serviceable_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_reattempt_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_reattempt_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_reattempt_tile")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_reattempt_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_reattempt_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=11,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_all_dashboard_reattempt_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=11,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_reattempt_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    order_status=11,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_reattempt_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=11,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["reattempt_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_ofd_tile")
            or request.user.has_perm("dashboard.can_view_own_dashboard_ofd_tile")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_ofd_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_ofd_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_ofd_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=12,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_own_dashboard_ofd_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=12,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_ofd_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    order_status=12,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_ofd_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=12,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["ofd_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_lost_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_lost_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_lost_tile")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_lost_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_lost_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=14,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_all_dashboard_lost_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=14,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_lost_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_teamlead,
                    order_status=14,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_lost_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=14,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["lost_tile_count"] = orders_count
        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_ndr_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_ndr_tile")
            or request.user.has_perm("dashboard.can_view_manager_dashboard_ndr_tile")
            or request.user.has_perm("dashboard.can_view_teamlead_dashboard_ndr_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_ndr_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=36,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_all_dashboard_ndr_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=36,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_ndr_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=36,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_ndr_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by__in=user_ids_for_manager,
                    order_status=36,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["ndr_tile_count"] = orders_count
        return Response(
            {
                "status": True,
                "message": "Data fetched successfully ",
                "data": tiles_count,
                "errors": None,
            },
            status=status.HTTP_200_OK,
        )

class TeamOrderListForDashboard(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        data={}
        if (request.user.has_perm("dashboard.can_view_own_dashboard_team_order_list") or request.user.has_perm("dashboard.can_view_all_dashboard_team_order_list") or request.user.has_perm("dashboard.can_view_manager_dashboard_team_order_list") or request.user.has_perm("dashboard.can_view_teamlead_dashboard_team_order_list") or request.user.profile.user_type=='admin'):
            if request.user.has_perm("dashboard.can_view_own_dashboard_team_order_list"):
                pass
            elif request.user.has_perm("dashboard.can_view_all_dashboard_team_order_list") or request.user.profile.user_type=='admin':
                teamlead_ids = UserProfile.objects.filter(branch=request.user.profile.branch, company=request.user.profile.company).values_list('teamlead', flat=True).distinct() 
                _teamleadTotalOrder=0
                _teamleadDailyTarget=0
                _teamleadTotalLead=0
                _teamleadAcceptedOrder=0
                _teamleadRejectedOrder=0
                _teamleadNoResponse=0 
                for teamlead_id in list(teamlead_ids):
                    if teamlead_id!=None:
                        _teamleaddat = User.objects.filter(id=teamlead_id).first()
                        if _teamleaddat:
                            _teamlead_serialized_data = UserSerializer(_teamleaddat).data
                        agent_ids = UserProfile.objects.filter(branch=request.user.profile.branch, company=request.user.profile.company,teamlead=teamlead_id).values_list('user', flat=True).distinct()
                        userDetailsDict={}
                        for agent_id in list(agent_ids):
                            user_profile = User.objects.filter(id=agent_id).first()
                            if user_profile:
                                _agent_serialized_data = UserSerializer(user_profile).data
                            _teamleadDailyTarget += _agent_serialized_data['profile']['daily_order_target']
                            _totalOrder = Order_Table.objects.filter(order_created_by=agent_id,branch=request.user.profile.branch,company=request.user.profile.company).count()
                            _teamleadTotalOrder += _totalOrder
                            _acceptedOrder = Order_Table.objects.filter(order_created_by=agent_id,branch=request.user.profile.branch,company=request.user.profile.company,order_status=2).count()
                            _teamleadAcceptedOrder += _acceptedOrder
                            _rejectedOrder = Order_Table.objects.filter(order_created_by=agent_id,branch=request.user.profile.branch,company=request.user.profile.company,order_status=3).count()
                            _noResponse = Order_Table.objects.filter(order_created_by=agent_id,branch=request.user.profile.branch,company=request.user.profile.company,order_status=4).count()
                            userDetailsDict[agent_id]={"id":agent_id,"total_order":_totalOrder,"daily_target":_agent_serialized_data['profile']['daily_order_target'],"name":_agent_serialized_data['username'],"total_Lead":100,"accepted_order":_acceptedOrder,"rejected_order":_rejectedOrder,"no_response":_noResponse}
                            data[teamlead_id]=userDetailsDict
                        userDetailsDict["teamleadTiles"]={"lead_id":teamlead_id,"teamlead_name":_teamlead_serialized_data['username'],"total_order":_teamleadTotalOrder,"daily_target":_teamleadDailyTarget,"total_lead":_teamleadTotalLead,"accepted_order":_teamleadAcceptedOrder,"oejected_order":_teamleadRejectedOrder,"no_response":_teamleadNoResponse}
                        _teamleadTotalOrder, _teamleadDailyTarget, _teamleadTotalLead, _teamleadAcceptedOrder, _teamleadRejectedOrder, _teamleadNoResponse = (0, 0, 0, 0, 0, 0)

            elif request.user.has_perm("dashboard.can_view_manager_dashboard_team_order_list"):
                pass
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_team_order_list"):
                pass
        return Response(
            {
                "status": True,
                "message": "Data fetched successfully",
                "data": data,
                "errors": None,
            },
            status=status.HTTP_200_OK,
        )

# class TopShellingProduct(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         _orderDetails = Order_Table.objects.filter(branch=request.user.profile.branch,company=request.user.profile.company)
#         _orderSerializerData = OrderTableSerializer(_orderDetails, many=True).data
#         _productId = {}
#         for order in _orderSerializerData:
#             for product in order['order_details']:
#                 product_name = product['product_name']
#                 product_qty = product['product_qty']
#                 product_mrp = product['product_mrp']
#                 price = product_mrp * product_qty
#                 order_id = product['order']

#                 if product_name in _productId:
#                     if _productId[product_name]['orderId'] != order_id:
#                         _productId[product_name]['order_count'] += 1
#                         _productId[product_name]['orderId'] = order_id
                        
#                     _productId[product_name]['unit'] += product_qty
#                     _productId[product_name]['total_shell_in_rupee'] = _productId[product_name]['unit']*product_mrp
#                 else:
#                     _productId[product_name] = {
#                         "unit": product_qty,
#                         "total_shell_in_rupee": price,
#                         "product_price": product_mrp,
#                         "product_image": "-------------------",
#                         "orderId": order_id,
#                         "order_count": 1
#                     }

#         return Response(
#             {
#                 "status": True,
#                 "message": "Data fetched successfully",
#                 "data": _productId,
#                 "errors": None,
#             },
#             status=status.HTTP_200_OK,
#         )


class TopShellingProduct(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        _branch = request.user.profile.branch_id
        if 'branch' in request.GET and request.GET['branch']:
            _branch = request.GET['branch']
            
        orders = Order_Table.objects.filter(
            branch=_branch,
            company=request.user.profile.company
        )
        serialized_orders = OrderTableSerializer(orders, many=True).data
        product_summary = self._summarize_products(serialized_orders)
        
        return Response(
            {
                "status": True,
                "message": "Data fetched successfully",
                "data": product_summary,
                "errors": None,
            },
            status=status.HTTP_200_OK,
        )

    def _summarize_products(self, orders):
        product_summary = {}

        for order in orders:
            for product in order['order_details']:
                product_name = product['product_name']
                product_qty = product['product_qty']
                product_mrp = product['product_mrp']
                order_id = product['order']
                total_price = product_mrp * product_qty

                if product_name in product_summary:
                    self._update_product_summary(product_summary[product_name], product_qty, order_id, total_price)
                else:
                    product_summary[product_name] = self._create_new_product_entry(
                        product_qty, total_price, product_mrp, order_id
                    )

        return product_summary

    def _update_product_summary(self, product_data, qty, order_id, total_price):
        if product_data['orderId'] != order_id:
            product_data['order_count'] += 1
            product_data['orderId'] = order_id

        product_data['unit'] += qty
        product_data['total_shell_in_rupee'] = product_data['unit'] * product_data['product_price']

    def _create_new_product_entry(self, qty, total_price, price, order_id):
        return {
            "unit": qty,
            "total_shell_in_rupee": total_price,
            "product_price": price,
            "product_image": "-------------------",
            "orderId": order_id,
            "order_count": 1
        }

class ScheduleOrderForDashboard(APIView):
    def get(self, request, *args, **kwargs):
        try:
            _branch = request.user.profile.branch_id
            start_datetime, end_datetime = self.get_date_range(request)
            if 'branch' in request.GET and request.GET['branch']:
                _branch = request.GET['branch']

            scheduled_count = self.get_order_count(is_scheduled=1, branch=_branch, start_datetime=start_datetime, end_datetime=end_datetime)
            non_scheduled_count = self.get_order_count(is_scheduled=0, branch=_branch, start_datetime=start_datetime, end_datetime=end_datetime)
            return Response(
                {
                    "status": True,
                    "message": "Data fetched successfully",
                    "data": {
                        "non_scheduled": non_scheduled_count,
                        "scheduled": scheduled_count,
                    },
                    "errors": None,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"status": False, "message": "An error occurred", "data": {}, "errors": True},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_date_range(self, request):
        """Extract and validate the date range from the request."""
        if 'date_range' in request.GET and request.GET['date_range']:
            date_range = request.GET['date_range'].split(' ')
            if len(date_range) != 2:
                raise ValueError("Date Range invalid")
            start_datetime = datetime.fromisoformat(date_range[0])
            end_datetime = datetime.fromisoformat(date_range[1])
            return start_datetime, end_datetime
        else:
            today = datetime.now()
            return datetime(today.year, today.month, 1), today

    def get_order_count(self, is_scheduled, branch, start_datetime, end_datetime):
        """Count orders based on scheduling status."""
        return Order_Table.objects.filter(
            is_scheduled=is_scheduled,
            branch=branch,
            company=self.request.user.profile.company,
            updated_at__range=(start_datetime, end_datetime),
        ).count()

class StateWiseSalesTracker(APIView):
    def get(self, request, *args: tuple, **kwargs: dict) -> Response:
        try:
            dashboard = ScheduleOrderForDashboard()
            _branch = request.user.profile.branch_id
            start_datetime, end_datetime = dashboard.get_date_range(request)
            if 'branch' in request.GET and request.GET['branch']:
                _branch = request.GET['branch']

            orders_data = (
                Order_Table.objects.filter(
                    branch=_branch,
                    company=request.user.profile.company,
                    updated_at__range=(start_datetime, end_datetime),
                )
                .values('customer_state')
                .annotate(count=Count('id'))
            )

            state_mapping = {state.id: state.name for state in Customer_State.objects.all()}
            state_counts = {
                state_mapping.get(entry['customer_state'], 'Unknown'): entry['count']
                for entry in orders_data
            }

            if not state_counts:
                return Response(
                    {
                        "status": True,
                        "message": "No data found for the specified criteria.",
                        "data": state_counts,
                        "errors": None,
                    },
                    status=status.HTTP_204_NO_CONTENT,
                )

            return Response(
                {
                    "status": True,
                    "message": "Data fetched successfully",
                    "data": state_counts,
                    "errors": None,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error fetching state-wise sales data: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(
                {
                    "status": False,
                    "message": "An error occurred while fetching data.",
                    "data": None,
                    "errors": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
class InvoiceDataForDashboard(APIView):
    def get(self, request, *args: tuple, **kwargs: dict) -> Response:
        dashboard = ScheduleOrderForDashboard()
        _branch = request.user.profile.branch_id

        try:
            start_datetime, end_datetime = dashboard.get_date_range(request)
        except Exception as e:
            logger.error(f"Error fetching date range: {e}")
            return Response(
                {
                    "status": False,
                    "message": "Error fetching date range.",
                    "errors": True,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if 'branch' in request.GET and request.GET['branch']:
            _branch = request.GET['branch']
        
        try:
            orders_data = Order_Table.objects.filter(
                branch=_branch,
                company=request.user.profile.company,
                updated_at__range=(start_datetime, end_datetime),
            )
        except Exception as e:
            logger.error(f"Error fetching orders data: {e}")
            return Response(
                {
                    "status": False,
                    "message": "Error fetching orders data.",
                    "errors": True,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        data = {
            'unpaid_amount': {'count': 0, 'amount': 0},
            'paid_amount': {'count': 0, 'amount': 0},
            'cancel_amount': {'count': 0, 'amount': 0},
            'sent_amount': {'count': 0, 'amount': 0},
        }

        if orders_data.exists():
            for row in orders_data:
                try:
                    if (row.payment_status.id == 1 or row.payment_status.id == 3) and row.order_status.id != 3 and row.is_scheduled == 0:
                        data['unpaid_amount']['count'] += 1
                        data['unpaid_amount']['amount'] += (row.gross_amount - row.prepaid_amount)
                    elif row.payment_status.id == 2:
                        data['paid_amount']['count'] += 1
                        data['paid_amount']['amount'] += row.gross_amount
                    elif row.order_status.id == 3:
                        data['cancel_amount']['count'] += 1
                        data['cancel_amount']['amount'] += row.gross_amount
                    elif row.is_scheduled == 1:
                        data['sent_amount']['count'] += 1
                        data['sent_amount']['amount'] += row.gross_amount
                except Exception as e:
                    logger.error(f"Error processing order ID {row.id}: {e}")

        return Response(
            {
                "status": True,
                "message": "Data fetched successfully",
                "data": data,
                "errors": False,
            },
            status=status.HTTP_200_OK,
        )
class SalesForecastDashboard(APIView):
    def get(self, request, *args: tuple, **kwargs: dict) -> Response:
        dashboard = ScheduleOrderForDashboard()
        _branch = request.user.profile.branch_id

        try:
            start_datetime, end_datetime = dashboard.get_date_range(request)
        except Exception as e:
            logger.error(f"Error fetching date range: {e}")
            return Response(
                {
                    "status": False,
                    "message": "Error fetching date range.",
                    "errors": True,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if 'branch' in request.GET and request.GET['branch']:
            _branch = request.GET['branch']
        
        try:
            orders_data = Order_Table.objects.filter(
                branch=_branch,
                company=request.user.profile.company,
                updated_at__range=(start_datetime, end_datetime),
            )
        except Exception as e:
            logger.error(f"Error fetching orders data: {e}")
            return Response(
                {
                    "status": False,
                    "message": "Error fetching orders data.",
                    "errors": True,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        data = {}
        if orders_data.exists():
            for row in orders_data:
                try:
                    status_name = row.order_status.name
                    if status_name in data:
                        data[status_name]['count'] += 1
                        data[status_name]['amount'] += row.gross_amount
                    else:
                        data[status_name] = {
                            'count': 1,
                            'amount': row.gross_amount,
                        }
                except Exception as e:
                    logger.error(f"Error processing order with ID {row.id}: {e}")

        return Response(
            {
                "status": True,
                "message": "Data fetched successfully",
                "data": data,
                "errors": False,
            },
            status=status.HTTP_200_OK,
        )
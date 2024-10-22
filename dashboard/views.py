from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from orders.models import Order_Table
from django.utils import timezone
from datetime import datetime
class GetUserDashboardtiles(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        start_datetime = datetime(2024, 1, 1, 0, 0)
        end_datetime = datetime(2024, 10, 22, 23, 59)
        tiles_count = {}
        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_running_tile")
            or request.user.has_perm(
                "dashboard.can_view_manager_dashboard_running_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_running_tile"
            )
            or request.user.has_perm("dashboard.can_view_all_dashboard_running_tile")
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_running_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm("dashboard.can_view_all_dashboard_running_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_manager_dashboard_running_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    created_at__range=(start_datetime, end_datetime),
                    # updated_at__range=(start_datetime, end_datetime)
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_running_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    created_at__range=(start_datetime, end_datetime),
                ).count()

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_Pending_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_Pending_tile")
            or request.user.has_perm(
                "dashboard.can_view_manager_dashboard_Pending_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_Pending_tile"
            )
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_Pending_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=1,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm("dashboard.can_view_all_dashboard_Pending_tile"):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=1,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_manager_dashboard_Pending_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=1,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_Pending_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=1,
                    created_at__range=(start_datetime, end_datetime),
                    updated_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["pending_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_all_dashboard_repeat_order_tile")
            or request.user.has_perm(
                "dashboard.can_view_own_dashboard_repeat_order_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_manager_dashboard_repeat_order_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_repeat_order_tile"
            )
        ):
            if request.user.has_perm(
                "dashboard.can_view_own_dashboard_repeat_order_tile"
            ):
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
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_repeat_order_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    repeat_order=1,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_manager_dashboard_repeat_order_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    repeat_order=1,
                    created_at__range=(start_datetime, end_datetime),
                    updated_at__range=(start_datetime, end_datetime),
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
                    branch=request.user.profile.branch,
                    order_status=3,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_all_dashboard_rejected_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=3,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_rejected_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=3,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_manager_dashboard_rejected_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=3,
                    created_at__range=(start_datetime, end_datetime),
                    # updated_at__range=(start_datetime, end_datetime)
                ).count()
            tiles_count["rejected_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_in_transit_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_in_transit_tile")
            or request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_in_transit_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_manager_dashboard_in_transit_tile"
            )
        ):
            if request.user.has_perm(
                "dashboard.can_view_all_dashboard_in_transit_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
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
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_in_transit_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=6,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_manager_dashboard_in_transit_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=6,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["in-transit_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_accepted_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_accepted_tile")
            or request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_accepted_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_manager_dashboard_accepted_tile"
            )
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_accepted_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=2,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_all_dashboard_accepted_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=2,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_accepted_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=2,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_manager_dashboard_accepted_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=2,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["accepted_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_all_dashboard_no_response_tile")
            or request.user.has_perm(
                "dashboard.can_view_own_dashboard_no_response_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_no_response_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_manager_dashboard_no_response_tile"
            )
        ):
            if request.user.has_perm(
                "dashboard.can_view_own_dashboard_no_response_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=4,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_all_dashboard_no_response_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=4,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_no_response_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=4,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_manager_dashboard_no_response_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=4,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["no_response_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_future_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_future_tile")
            or request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_future_tile"
            )
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
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_future_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=5,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
                tiles_count["running_tile_count"] = orders_count
            elif request.user.has_perm(
                "dashboard.can_view_manager_dashboard_future_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=5,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["future_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_delivered_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_delivered_tile")
            or request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_delivered_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_manager_dashboard_delivered_tile"
            )
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_delivered_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=7,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_all_dashboard_delivered_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=7,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_delivered_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=7,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_manager_dashboard_delivered_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=7,
                    created_at__range=(start_datetime, end_datetime),
                ).count()

            tiles_count["delivered_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_in_transit_rto")
            or request.user.has_perm("dashboard.can_view_all_dashboard_in_transit_rto")
            or request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_in_transit_rto"
            )
            or request.user.has_perm(
                "dashboard.can_view_manager_dashboard_in_transit_rto"
            )
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_delivered_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=8,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_all_dashboard_in_transit_rto"
            ):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=8,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_in_transit_rto"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=8,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_manager_dashboard_in_transit_rto"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
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
                    order_created_by=request.user.id,
                    order_status=9,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_rto"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=9,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["rto_tile_count"] = orders_count

        if (
            request.user.has_perm(
                "dashboard.can_view_own_dashboard_non_serviceable_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_all_dashboard_non_serviceable_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_non_serviceable_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_manager_dashboard_non_serviceable_tile"
            )
        ):
            if request.user.has_perm(
                "dashboard.can_view_own_dashboard_non_serviceable_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=10,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_all_dashboard_non_serviceable_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=10,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_teamlead_dashboard_rto"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=10,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm("dashboard.can_view_manager_dashboard_rto"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=10,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            tiles_count["non_serviceable_tile_count"] = orders_count

        if (
            request.user.has_perm("dashboard.can_view_own_dashboard_reattempt_tile")
            or request.user.has_perm("dashboard.can_view_all_dashboard_reattempt_tile")
            or request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_reattempt_tile"
            )
            or request.user.has_perm(
                "dashboard.can_view_manager_dashboard_reattempt_tile"
            )
        ):
            if request.user.has_perm("dashboard.can_view_own_dashboard_reattempt_tile"):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    branch=request.user.profile.branch,
                    order_status=11,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_all_dashboard_reattempt_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    branch=request.user.profile.branch,
                    order_status=11,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_reattempt_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=11,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_manager_dashboard_reattempt_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
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
                    order_created_by=request.user.id,
                    order_status=12,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_ofd_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
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
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_lost_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
                    order_status=14,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_manager_dashboard_lost_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
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
                    order_created_by=request.user.id,
                    order_status=36,
                    created_at__range=(start_datetime, end_datetime),
                ).count()
            elif request.user.has_perm(
                "dashboard.can_view_teamlead_dashboard_ndr_tile"
            ):
                orders_count = Order_Table.objects.filter(
                    order_created_by=request.user.id,
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

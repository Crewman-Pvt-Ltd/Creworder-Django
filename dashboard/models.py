from django.db import models

class DashboardTiles(models.Model):
    class Meta:
        permissions = (
            ('can_view_own_dashboard_running_tile', 'Can view own dashboard running tile'),
            ('can_view_manager_dashboard_running_tile', 'Can view manager dashboard running tile'),
            ('can_view_teamlead_dashboard_running_tile', 'Can view team lead dashboard running tile'),
            ('can_view_own_dashboard_Pending_tile', 'Can view own dashboard Pending tile'),
            ('can_view_manager_dashboard_Pending_tile', 'Can view manager dashboard Pending tile'),
            ('can_view_teamlead_dashboard_Pending_tile', 'Can view team lead dashboard Pending tile'),
            ('can_view_own_dashboard_repeat_order_tile', 'Can view own dashboard repeat_order tile'),
            ('can_view_manager_dashboard_repeat_order_tile', 'Can view manager dashboard repeat_order tile'),
            ('can_view_teamlead_dashboard_repeat_order_tile', 'Can view team lead dashboard repeat_order tile'),
            ('can_view_own_dashboard_rejected_tile', 'Can view own dashboard rejected tile'),
            ('can_view_manager_dashboard_rejected_tile', 'Can view manager dashboard rejected tile'),
            ('can_view_teamlead_dashboard_rejected_tile', 'Can view team lead dashboard rejected tile'),
            ('can_view_own_dashboard_in_transit_tile', 'Can view own dashboard in transit tile'),
            ('can_view_manager_dashboard_in_transit_tile', 'Can view manager dashboard in transit tile'),
            ('can_view_teamlead_dashboard_in_transit_tile', 'Can view team lead dashboard in transit tile'),
            ('can_view_own_dashboard_accepted_tile', 'Can view own dashboard accepted tile'),
            ('can_view_manager_dashboard_accepted_tile', 'Can view manager dashboard accepted tile'),
            ('can_view_teamlead_dashboard_accepted_tile', 'Can view team lead dashboard accepted tile'),
            ('can_view_own_dashboard_no_response_tile', 'Can view own dashboard no response tile'),
            ('can_view_manager_dashboard_no_response_tile', 'Can view manager dashboard no response tile'),
            ('can_view_teamlead_dashboard_no_response_tile', 'Can view team lead dashboard no response tile'),
            ('can_view_own_dashboard_total_tile', 'Can view own dashboard total tile'),
            ('can_view_manager_dashboard_total_tile', 'Can view manager dashboard total tile'),
            ('can_view_teamlead_dashboard_total_tile', 'Can view team lead dashboard total tile'),
            ('can_view_own_dashboard_future_tile', 'Can view own dashboard future tile'),
            ('can_view_manager_dashboard_future_tile', 'Can view manager dashboard future tile'),
            ('can_view_teamlead_dashboard_future_tile', 'Can view team lead dashboard future tile'),
            ('can_view_own_dashboard_delivered_tile', 'Can view own dashboard delivered tile'),
            ('can_view_manager_dashboard_delivered_tile', 'Can view manager dashboard delivered tile'),
            ('can_view_teamlead_dashboard_delivered_tile', 'Can view team lead dashboard delivered tile'),
            ('can_view_own_dashboard_schedule_order_chart', 'Can view own dashboard schedule order chart'),
            ('can_view_manager_dashboard_schedule_order_chart', 'Can view manager dashboard schedule order chart'),
            ('can_view_teamlead_dashboard_schedule_order_chart', 'Can view team lead dashboard schedule order chart'),
            ('can_view_own_dashboard_sales_forecast_chart', 'Can view own dashboard sales forecast chart'),
            ('can_view_manager_dashboard_sales_forecast_chart', 'Can view manager dashboard sales forecast chart'),
            ('can_view_teamlead_dashboard_sales_forecast_chart', 'Can view team lead dashboard sales forecast chart'),
            ('can_view_own_dashboard_top_selling_list', 'Can view own dashboard top selling list'),
            ('can_view_manager_dashboard_top_selling_list', 'Can view manager dashboard top selling list'),
            ('can_view_teamlead_dashboard_top_selling_list', 'Can view team lead dashboard top selling list'),
            ('can_view_own_dashboard_team_order_list', 'Can view own dashboard team order list'),
            ('can_view_manager_dashboard_team_order_list', 'Can view manager dashboard team order list'),
            ('can_view_teamlead_dashboard_team_order_list', 'Can view team lead dashboard team order list'),
        )
        db_table ='dashboard_table'
    name=models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return f'{self.name}'
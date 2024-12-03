from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from accounts.models import Company, Branch

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)
class FollowUp(models.Model):
    FOLLOW_STATUS_CHOICES = [("pending", 'Pending'),("responded", 'Responded'),("deleted", 'Deleted'),]
    SNOOZE_CHOICES = [("pending", 'Pending'),("snooze", 'Snooze'),]
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(validators=[phone_regex], max_length=17, blank=False)
    reminder_date = models.DateTimeField()
    description = models.TextField()
    follow_status = models.CharField(max_length=255,choices=FOLLOW_STATUS_CHOICES)
    snooze = models.CharField(max_length=255,choices=SNOOZE_CHOICES)
    follow_add_by = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE) 
    call_id = models.CharField(max_length=50, null=True, blank=True)
    branch = models.ForeignKey(Branch, related_name="followup_branch", on_delete=models.CASCADE,blank=True, null=True,)
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, related_name="followup_company")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'follow_up_table'

    def __str__(self):
        return str(self.id)
    


class Notepad(models.Model):
    id = models.AutoField(primary_key=True)
    authID = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'notepad_table'
    def __str__(self):
        return f"Note {self.id} by {self.authID}"
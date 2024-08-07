from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ChatSession(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default='creworder')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'chat_session_table'

    def __str__(self):
        return str(self.id)
    
class Chat(models.Model):
    class ChatStatus(models.IntegerChoices):
        UNREAD = 0, 'Unread'  
        READ = 1, 'Read' 
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)
    massage_type = models.CharField(max_length=10, choices=[('media', 'Media'), ('text', 'Text')], default='text')    
    user = models.ForeignKey(User, related_name='chat_created_by', on_delete=models.CASCADE, default=1)
    from_user = models.ForeignKey(User, related_name='sent_chats', on_delete=models.CASCADE) 
    to_user = models.ForeignKey(User, related_name='received_chats', on_delete=models.CASCADE)
    chat_session = models.ForeignKey('ChatSession', on_delete=models.CASCADE, default=1)
    chat_status = models.IntegerField(choices=ChatStatus.choices, default=ChatStatus.UNREAD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'chat_detail_table'

    def __str__(self):
        return str(self.id)
   
class Group(models.Model):
    class GroupStatus(models.IntegerChoices):
        INACTIVE = 0, 'Inactive'  
        ACTIVE = 1, 'Active'
    id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=50)
    group_status = models.IntegerField(choices=GroupStatus.choices, default=GroupStatus.INACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'group_chat_table'

    def __str__(self):
        return str(self.group_name)
    
class GroupDetails(models.Model):
    class GroupMemberType(models.IntegerChoices):
        ADMIN = 0, 'Admin'  
        USER = 1, 'User'
    id = models.AutoField(primary_key=True)
    Group = models.ForeignKey(Group, related_name='group_id', on_delete=models.CASCADE) 
    Group_member = models.ForeignKey(User, related_name='group_member_id', on_delete=models.CASCADE)
    Group_member_status = models.IntegerField(choices=GroupMemberType.choices, default=GroupMemberType.USER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'group_delails_table'

    def __str__(self):
        return str(self.Group_member)

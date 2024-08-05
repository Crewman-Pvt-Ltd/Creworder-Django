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

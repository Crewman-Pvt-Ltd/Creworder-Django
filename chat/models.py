from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Chat(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)
    massage_type = models.CharField(max_length=10, choices=[('media', 'Media'), ('text', 'Text')], default='text')
    user = models.ForeignKey(User, related_name='chat_created_by', on_delete=models.CASCADE, default=1) 
    from_user = models.ForeignKey(User, related_name='sent_chats', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_chats', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'chat_table'

    def __str__(self):
        return str(self.id)

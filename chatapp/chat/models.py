from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Conversation(models.Model):

    CONVERSATION_TYPE_CHOICES = (
        ('direct','Direct'),
        ('group','Group'),
    )

    type = models.CharField(
        max_length=10,
        choices=CONVERSATION_TYPE_CHOICES
    )

    name = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name='created_conversations'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        if self.type == 'group':
            return self.name or f'Group {self.id}'
        return f'Direct Chat {self.id}'
    
class ConversationMember(models.Model):

    ROLE_CHOICES = (
        ('admin','Admin'),
        ('member','Member'),
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='members'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversations'
    )

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='member'
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('conversation','user')

    def __str__(self):
        return f'{self.user.username} in Conversation {self.Conversation.id}'
    
class Message(models.Model):
    MESSAGE_TYPE_CHOICES = (
        ('text','Text'),
        ('image','Image'),
        ('file','File'),
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    content = models.TextField(blank=True,null=True)

    file = models.FileField(
        upload_to='chat_files/',
        blank=True,
        null=True
    )

    message_type = models.CharField(
        max_length=50,
        choices=MESSAGE_TYPE_CHOICES,
        default='text'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Message {self.id} by {self.sender.username}'
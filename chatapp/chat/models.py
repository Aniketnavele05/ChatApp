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

    Conversation = models.ForeignKey(
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

    joined_at = models.DateTimeField(auto_now_add=False)

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('conversation','user')

    def __str__(self):
        return f'{self.user.username} in Conversation {self.Conversation.id}'
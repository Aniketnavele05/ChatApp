from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, ConversationMember


class ConversationCreateSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=Conversation.CONVERSATION_TYPE_CHOICES)
    name = serializers.CharField(required=False,allow_blank=True)
    members = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False
    )

    def validate(self,data):
        user = self.context['request'].user
        members = data['members']

        members = list(set(members)-{user.id})

        if data['type'] == 'direct' and len(members) != 1:
            raise serializers.ValidationError(
                "Direct chat must have exactly one other user."
            )
        
        if data['type'] == 'group' and len(members) < 1:
            raise serializers.ValidationError(
                "Group chat must at least one member,."
            )
        
        data['members'] = members
        return data
    
class ConverrsationListSerializer(serializers.Serializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id',
            'type',
            'name',
            'created_at',
            'last_message',
        ]

        def get_last_message(Self,obj):
            message = obj.messages.last()
            if not message:
                return None
            
            return {
                'content':message.content,
                'sender':message.sender.username,
                'created_at':message.created_at
            }
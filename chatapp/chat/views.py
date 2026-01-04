from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction
from .models import Conversation,ConversationMember
from .serializer import ConversationCreateSerializer

# Create your views here.

class ConversationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = ConversationCreateSerializer(
            data=request.data,
            context={'request':request}
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = serializer.validated_data
        members = data['members']

        with transaction.atomic():
            conversation = Conversation.objects.create(
                type = data['type'],
                name = data.get('name'),
                created_by = request.user
            )

            conversationMember = ConversationMember.objects.create(
                conversation = conversation,
                user = request.user,
                role = 'admin'
            )

            users = User.objects.filter(id__in=members)

            for user in users:
                ConversationMember.objects.create(
                    conversation=conversation,
                    user=user,
                    role='member'
                )
        
        return Response(
            {
                'message': 'Conversation created successfully',
                'conversation_id': conversation.id
            },
            status=status.HTTP_201_CREATED
        )
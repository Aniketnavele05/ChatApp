from django.urls import path
from .views import ConversationCreateView,ConversationListView

urlpatterns = [
    path('conversation/',ConversationListView.as_view()),
    path('conversation/create/',ConversationCreateView.as_view()),
]

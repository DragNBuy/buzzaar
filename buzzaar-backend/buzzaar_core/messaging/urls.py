from django.urls import path
from . import views

urlpatterns = [
    path("", views.ConversationView.as_view(), name="convo_view"),
    path("<int:convo_id>/", views.get_conversation, name="get_conversation"),
]

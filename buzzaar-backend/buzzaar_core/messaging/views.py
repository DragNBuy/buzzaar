from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser as User

from .models import Conversation
from .serializers import ConversationListSerializer, ConversationSerializer


class ConversationView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            username = data.pop("username")
        except KeyError:
            msg = {
                "message": "Missing username property of the recipient in the request body."
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        if request.user.username == username:
            msg = {"message": "You cannot create a conversation with yourself."}
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        participant = get_object_or_404(User, username=username)
        convo = Conversation.objects.filter(
            Q(initiator=request.user, receiver=participant)
            | Q(initiator=participant, receiver=request.user)
        )
        if convo.exists():
            return redirect(reverse("get_conversation", args=(convo[0].id,)))
        else:
            convo = Conversation.objects.create(
                initiator=request.user, receiver=participant
            )
        return Response(ConversationSerializer(instance=convo).data)

    def get(self, request, *args, **kwargs):
        conversation_list = Conversation.objects.filter(
            Q(initiator=request.user) | Q(receiver=request.user)
        )
        serializer = ConversationListSerializer(instance=conversation_list, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def get_conversation(request, convo_id):
    conversation = get_object_or_404(Conversation, pk=convo_id)
    serializer = ConversationSerializer(conversation)
    return Response(serializer.data)

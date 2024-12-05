from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import CustomUser as User

from .models import Conversation
from .serializers import ConversationListSerializer, ConversationSerializer


@api_view(["POST"])
def start_convo(request):
    data = request.data
    try:
        user_id = data.pop("user_id")
    except KeyError:
        msg = {"message": "Missing user_id property of the recipient in the request body."}
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    if request.user.id == user_id:
        msg = {"message": "You cannot create a conversation with yourself."}
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    participant = get_object_or_404(User, pk=user_id)
    convo = Conversation.objects.filter(
        Q(initiator=request.user, receiver=participant)
        | Q(initiator=participant, receiver=request.user)
    )
    if convo.exists():
        return redirect(reverse('get_conversation', args=(convo[0].id,)))
    else:
        convo = Conversation.objects.create(
            initiator=request.user,
            receiver=participant
        )
        return Response(ConversationSerializer(instance=convo).data)


@api_view(["GET"])
def get_conversation(request, convo_id):
    conversation = Conversation.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({"message": "Conversation does not exist"})
    else:
        serializer = ConversationSerializer(instance=conversation[0])
        return Response(serializer.data)


@api_view(["GET"])
def conversations(request):
    conversation_list = Conversation.objects.filter(
        Q(initiator=request.user) | Q(receiver=request.user)
    )
    serializer = ConversationListSerializer(instance=conversation_list)
    return Response(serializer.data)

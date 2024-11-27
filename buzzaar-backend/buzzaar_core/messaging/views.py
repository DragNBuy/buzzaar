from django.shortcuts import render, get_object_or_404
from .models import Conversation
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import CustomUser as User
from .serializers import ConversationSerializer, ConversationListSerializer
from django.db.models import Q
from django.shortcuts import redirect, reverse

@api_view(['POST'])
def start_convo(request):
    data = request.data
    username = data.pop('username')
    participant = get_object_or_404(User, username=username)
    convo = Conversation.objects.filter(Q(buyer=request.user, seller=participant) |
                                        Q(buyer=participant, seller=request.user))
    if convo.exists():
        return redirect(reverse('get_conversation', args=convo[0].id))
    else:
        convo = Conversation.objects.create(
            buyer=request.user,
            seller=participant
        )
        return Response(ConversationSerializer(instance=convo).data)

@api_view(['GET'])
def get_conversation(request, convo_id):
    conversation = Conversation.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({ 'message': 'Conversation does not exist' })
    else:
        serializer = ConversationSerializer(instance=conversation[0])
        return Response(serializer.data)

@api_view(['GET'])
def conversations(request):
    conversation_list = Conversation.objects.filter(Q(buyer=request.user) | Q(seller=request.user))
    serializer = ConversationListSerializer(instance=conversation_list)
    return Response(serializer.data)

from dj_rest_auth.registration.views import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import UserLike
from .serializers import UserLikeSerializer


class UserLikeViewSet(ModelViewSet):
    queryset = UserLike.objects.all()
    serializer_class = UserLikeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['user', 'product']

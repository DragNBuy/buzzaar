from dj_rest_auth.registration.views import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import UserLike
from .serializers import UserLikeSerializer


class UserLikeViewSet(ModelViewSet):
    queryset = UserLike.objects.all()
    serializer_class = UserLikeSerializer
    permission_classes = [IsAuthenticated]

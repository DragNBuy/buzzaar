from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CustomUser as User
from .serializers import CustomUserSerializer as UserSerializer


@api_view(["GET"])
def get_users(request):
    users = User.objects.all().order_by("-email")
    serializer = UserSerializer(instance=users, many=True)
    return Response(serializer.data)

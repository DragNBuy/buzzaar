from dj_rest_auth.registration.views import IsAuthenticated
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


# use this to get CSRF token
def helloworld(request):
    return render(request, "hello.html")

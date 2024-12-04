from dj_rest_auth.registration.views import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Product, ProductPicture
from .serializers import ProductPictureSerializer, ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class ProductPictureViewSet(ModelViewSet):
    queryset = ProductPicture.objects.all()
    serializer_class = ProductPictureSerializer
    permission_classes = [IsAuthenticated]

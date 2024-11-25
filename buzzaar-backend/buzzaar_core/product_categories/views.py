from dj_rest_auth.registration.views import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import ProductCategory
from .serializers import ProductCategorySerializer


class ProductCategoryViewSet(ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [IsAuthenticated]

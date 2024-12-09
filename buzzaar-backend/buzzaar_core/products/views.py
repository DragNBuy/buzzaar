from dj_rest_auth.registration.views import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Product, ProductReport
from .serializers import ProductReportSerializer, ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]


class AllProductReportViewSet(ReadOnlyModelViewSet):
    queryset = ProductReport.objects.all()
    serializer_class = ProductReportSerializer


class ProductReportViewSet(ModelViewSet):
    serializer_class = ProductReportSerializer

    def get_queryset(self):
        product_id = self.kwargs.get("product_pk")
        return ProductReport.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get("product_pk")
        product = get_object_or_404(Product, pk=product_id)
        serializer.save(product=product)

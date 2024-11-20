from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializer


def listProducts(request):
    products = list(Product.objects.all().values())
    return JsonResponse(products, safe=False)


def getProduct(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({"status": f"Product id={product_id} not found"})

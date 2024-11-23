from django.http import JsonResponse
from django.db import DataError
from django.shortcuts import render
from .models import Product
from .serializers import ProductSerializer
from users.models import CustomUser
import json
import datetime
from rest_framework.viewsets import ModelViewSet


class ProductViewSet(ModelViewSet):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables permission

    def list(self, request):
        products = list(Product.objects.all().values())
        return JsonResponse(products, safe=False)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return JsonResponse(serializer.data, safe=False)
        except Product.DoesNotExist:
            return JsonResponse({"status": "fail", "message": f"Product id={pk} not found"})

    def create(self, request):
        json_data = json.loads(request.body)

        owner_id = json_data['owner_id']
        title = json_data['title']
        description = json_data['description']
        price = json_data['price']

        try:
            user = CustomUser.objects.get(pk=owner_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({"status": "fail", "message": f"User id={owner_id} not found"}, status=424)

        try:
            product = Product.objects.create(
                owner=user,
                title=title,
                description=description,
                initial_asking_price=price,
                date_created=datetime.datetime.now(),
                visible=True
            )
        except DataError:
            return JsonResponse({"status": "fail", "message": "Price can only have 6 digits before floating point and 2 after"}, status=400)
        except Exception:
            return JsonResponse({"status": "fail", "message": "Failed to create product"}, status=400)

        return JsonResponse({"status": "ok", "message": f"product id={product.pk} created"}, status=201)

    def destroy(self, request, pk=None):
        try:
            Product.objects.filter(id=pk).delete()
        except ValueError:
            return JsonResponse({"status": "fail", "message": "id must be an integer"})

        return JsonResponse({"status": "ok", "message": f"deleted product id={pk}"})


# use this to get CSRF token
def helloworld(request):
    return render(request, "hello.html")

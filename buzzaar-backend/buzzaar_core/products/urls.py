from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.listProducts),
    path("product/<int:product_id>", views.getProduct),
]

"""
URL configuration for buzzaar_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from dj_rest_auth.registration.views import VerifyEmailView
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from product_categories.views import ProductCategoryViewSet
from products.views import AllProductReportViewSet, ProductReportViewSet, ProductViewSet
from user_likes.views import UserLikeViewSet

router = routers.SimpleRouter()
router.register(r"api/products", ProductViewSet, basename="products")
router.register(
    r"api/product_categories", ProductCategoryViewSet, basename="product_categories"
)
router.register(r"api/user_likes", UserLikeViewSet, basename="user_likes")
router.register(r"api/reports", AllProductReportViewSet, basename="all_product_reports")

product_router = nested_routers.NestedSimpleRouter(
    router, r"api/products", lookup="product"
)
product_router.register(r"reports", ProductReportViewSet, basename="product-reports")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "api/auth/account-confirm-email/",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    path("", include("home.urls")),
    path("api/", include("products.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/chats/",
        include("messaging.urls"),
        name="chats",
    ),
    path("api/users/", include("users.urls"), name="users"),
]

urlpatterns += router.urls
urlpatterns += product_router.urls

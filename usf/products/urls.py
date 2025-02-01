from rest_framework.routers import SimpleRouter

from products.views import ProductViewSet, PublicProductViewSet

router = SimpleRouter()
router.register("products", ProductViewSet)
router.register("public/products", PublicProductViewSet, "public-product")

urlpatterns = router.urls

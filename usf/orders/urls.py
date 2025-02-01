from rest_framework.routers import SimpleRouter

from orders.views import OrderViewSet

router = SimpleRouter()
router.register("orders", OrderViewSet, "orders")

urlpatterns = router.urls

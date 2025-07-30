"""Nautobot Prometheus Service Discovery API URLs."""

from rest_framework import routers

from .views import DeviceViewSet, IPAddressViewSet, VirtualMachineViewSet

router = routers.DefaultRouter()
router.register("virtual-machines", VirtualMachineViewSet)
router.register("devices", DeviceViewSet)
router.register("ip-addresses", IPAddressViewSet)

urlpatterns = router.urls

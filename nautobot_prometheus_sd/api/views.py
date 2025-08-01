"""Nautobot Prometheus Service Discovery API Views."""

from nautobot.dcim.models.devices import Device
from nautobot.extras.api.views import CustomFieldModelViewSet as NautobotModelViewSet
from nautobot.ipam.filters import IPAddressFilterSet
from nautobot.ipam.models import IPAddress
from nautobot.virtualization.filters import VirtualMachineFilterSet
from nautobot.virtualization.models import VirtualMachine

from nautobot_prometheus_sd.filters import DeviceFilterSetCustom

from .serializers import (
    PrometheusDeviceSerializer,
    PrometheusIPAddressSerializer,
    PrometheusVirtualMachineSerializer,
)


class VirtualMachineViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """ViewSet for Virtual Machines to Prometheus target representation."""

    queryset = VirtualMachine.objects.prefetch_related(
        "cluster__location",
        "role",
        "tenant",
        "platform",
        "primary_ip4",
        "primary_ip6",
        "tags",
        "services",
    )
    filterset_class = VirtualMachineFilterSet
    serializer_class = PrometheusVirtualMachineSerializer
    pagination_class = None


class DeviceViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """ViewSet for Devices to Prometheus target representation."""

    queryset = Device.objects.prefetch_related(
        "device_type__manufacturer",
        "role",
        "tenant",
        "platform",
        "location",
        "location",
        "rack",
        "parent_bay",
        "virtual_chassis__master",
        "primary_ip4__nat_outside",
        "primary_ip6__nat_outside",
        "tags",
    )
    filterset_class = DeviceFilterSetCustom
    serializer_class = PrometheusDeviceSerializer
    pagination_class = None


class IPAddressViewSet(NautobotModelViewSet):  # pylint: disable=too-many-ancestors
    """ViewSet for IP Addresses to Prometheus target representation."""

    queryset = IPAddress.objects.prefetch_related("tenant", "tags")
    serializer_class = PrometheusIPAddressSerializer
    filterset_class = IPAddressFilterSet
    pagination_class = None

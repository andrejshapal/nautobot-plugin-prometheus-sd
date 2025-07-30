"""Serialize Nautobot objects to Prometheus target representation."""

from nautobot.dcim.models import Device
from nautobot.ipam.models import IPAddress
from nautobot.virtualization.models import VirtualMachine
from netaddr import IPNetwork
from rest_framework import serializers

from . import utils
from .utils import LabelDict


class PrometheusDeviceSerializer(serializers.ModelSerializer):
    """Serialize a device to Prometheus target representation."""

    class Meta:
        """Meta class for PrometheusDeviceSerializer."""

        model = Device
        fields = ["targets", "labels"]

    targets = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()

    def get_targets(self, obj):
        """Get the targets for the device."""
        return [obj.name]

    def get_labels(self, obj):
        """Get the labels for the device."""
        labels = LabelDict({"status": obj.status.name, "model": obj.__class__.__name__, "name": obj.name})

        utils.extract_primary_ip(obj, labels)
        utils.extracts_platform(obj, labels)
        utils.extract_tags(obj, labels)
        utils.extract_tenant(obj, labels)
        utils.extract_cluster(obj, labels)
        utils.extract_services(obj, labels)
        utils.extract_contacts(obj, labels)
        utils.extract_custom_fields(obj, labels)

        if hasattr(obj, "device_role") and obj.device_role is not None:
            labels["role"] = obj.device_role.name
            labels["role_slug"] = obj.device_role.slug

        if hasattr(obj, "device_type") and obj.device_type is not None:
            labels["device_type"] = obj.device_type.model
            labels["device_type_slug"] = obj.device_type.slug

        if hasattr(obj, "site") and obj.site is not None:
            labels["site"] = obj.site.name
            labels["site_slug"] = obj.site.slug

        return labels.get_labels()


class PrometheusVirtualMachineSerializer(serializers.ModelSerializer):
    """Serialize a virtual machine to Prometheus target representation."""

    class Meta:
        """Meta class for PrometheusVirtualMachineSerializer."""

        model = VirtualMachine
        fields = ["targets", "labels"]

    targets = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()

    def get_targets(self, obj):
        """Get the targets for the virtual machine."""
        return [obj.name]

    def get_labels(self, obj):
        """Get the labels for the virtual machine."""
        labels = LabelDict({"status": obj.status.name, "model": obj.__class__.__name__, "name": obj.name})

        utils.extract_primary_ip(obj, labels)
        utils.extracts_platform(obj, labels)
        utils.extract_tags(obj, labels)
        utils.extract_tenant(obj, labels)
        utils.extract_cluster(obj, labels)
        utils.extract_services(obj, labels)
        utils.extract_contacts(obj, labels)
        utils.extract_custom_fields(obj, labels)

        if hasattr(obj, "role") and obj.role is not None:
            labels["role"] = obj.role.name
            labels["role_slug"] = obj.role.slug

        return labels.get_labels()


class PrometheusIPAddressSerializer(serializers.ModelSerializer):
    """Serialize an IP address to Prometheus target representation."""

    class Meta:
        """Meta class for PrometheusIPAddressSerializer."""

        model = IPAddress
        fields = ["targets", "labels"]

    targets = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()

    def extract_ip(self, obj):
        """Extract the IP address from the IPAddress object."""
        return str(IPNetwork(obj.address).ip)

    def get_targets(self, obj):
        """Get the targets for the IP address."""
        if obj.dns_name:
            return [obj.dns_name]

        return [self.extract_ip(obj)]

    def get_labels(self, obj):
        """Get IP address labels."""
        labels = LabelDict(
            {
                "status": obj.status.name,
                "model": obj.__class__.__name__,
                "ip": self.extract_ip(obj),
            }
        )
        if obj.role:
            labels["role"] = obj.role

        utils.extract_tags(obj, labels)
        utils.extract_tenant(obj, labels)
        utils.extract_custom_fields(obj, labels)

        return labels.get_labels()

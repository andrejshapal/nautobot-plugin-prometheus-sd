"""Utility functions for Nautobot Prometheus SD tests."""

from nautobot.dcim.models import Device, DeviceRole, Platform
from nautobot.dcim.models.devices import DeviceType, Manufacturer
from nautobot.dcim.models.sites import Site
from nautobot.extras.models import Status
from nautobot.ipam.models import IPAddress
from nautobot.tenancy.models import Tenant, TenantGroup
from nautobot.virtualization.models import (
    Cluster,
    ClusterGroup,
    ClusterType,
    VirtualMachine,
)


def build_cluster():
    """Build a cluster object for testing purposes."""
    return Cluster.objects.get_or_create(
        name="DC1",
        group=ClusterGroup.objects.get_or_create(name="VMware")[0],
        type=ClusterType.objects.get_or_create(name="On Prem")[0],
        site=Site.objects.get_or_create(name="Campus A", slug="campus-a")[0],
    )[0]


def build_tenant():
    """Build a tenant object for testing purposes."""
    return Tenant.objects.get_or_create(name="Acme Corp.", slug="acme")[0]


def build_status():
    """Build a status object for testing purposes."""
    return Status.objects.get_or_create(
        name="Active",
        slug="active",
    )[0]


def build_custom_fields():
    """Build custom field definition with different kinds of custom values."""
    return {
        "contact": [{"id": 1, "url": "http://localhost:8000/api/tenancy/contacts/1/", "display": "Foo", "name": "Foo"}],
        "json": {"foo": ["bar", "baz"]},
        "multi_selection": ["foo", "baz"],
        "simple": "Foobar 123",
        "int": "42",
        "text_long": "This is\r\na  pretty\r\nlog\r\nText",
        "bool": "True",
    }


def build_minimal_vm(name):
    """Build a minimal virtual machine object for testing purposes."""
    return VirtualMachine.objects.get_or_create(name=name, cluster=build_cluster(), status=build_status())[0]


def build_vm_full(name):
    """Build a full virtual machine object for testing purposes."""
    vm = build_minimal_vm(name=name)  # pylint: disable=invalid-name
    vm.tenant = build_tenant()  # type: ignore
    vm.status = build_status()
    vm._custom_field_data = build_custom_fields()  # type: ignore # pylint: disable=protected-access
    vm.role = DeviceRole.objects.get_or_create(name="VM", slug="vm", vm_role=True)[0]  # type: ignore
    vm.platform = Platform.objects.get_or_create(  # type: ignore
        name="Ubuntu 20.04", slug="ubuntu-20.04"
    )[0]
    vm.primary_ip4 = IPAddress.objects.get_or_create(address="192.168.0.1/24")[0]  # type: ignore
    vm.primary_ip6 = IPAddress.objects.get_or_create(address="2001:db8:1701::2/64")[0]  # type: ignore

    vm.tags.add("Tag1")
    vm.tags.add("Tag 2")
    return vm


def build_minimal_device(name):
    """Build a minimal device object for testing purposes."""
    return Device.objects.get_or_create(
        name=name,
        status=build_status(),
        device_role=DeviceRole.objects.get_or_create(name="Firewall", slug="firewall")[0],
        device_type=DeviceType.objects.get_or_create(
            model="SRX",
            slug="srx",
            manufacturer=Manufacturer.objects.get_or_create(name="Juniper", slug="juniper")[0],
        )[0],
        site=Site.objects.get_or_create(name="Site", slug="site")[0],
    )[0]


def build_device_full(name):
    """Build a full device object for testing purposes."""
    device = build_minimal_device(name)
    device.tenant = build_tenant()  # type: ignore
    device.status = build_status()
    device._custom_field_data = build_custom_fields()  # type: ignore # pylint: disable=protected-access
    device.platform = Platform.objects.get_or_create(name="Junos", slug="junos")[0]  # type: ignore
    device.primary_ip4 = IPAddress.objects.get_or_create(address="192.168.0.1/24")[0]  # type: ignore
    device.primary_ip6 = IPAddress.objects.get_or_create(address="2001:db8:1701::2/64")[  # type: ignore
        0
    ]
    device.tags.add("Tag1")
    device.tags.add("Tag 2")
    return device


def build_minimal_ip(address):
    """Build a minimal IP address object for testing purposes."""
    return IPAddress.objects.get_or_create(address=address, status=build_status())[0]


def build_full_ip(address, dns_name=""):
    """Build a full IP address object for testing purposes."""
    ip = build_minimal_ip(address=address)  # pylint: disable=invalid-name
    ip.status = build_status()
    ip._custom_field_data = build_custom_fields()  # type: ignore # pylint: disable=protected-access
    ip.tenant = Tenant.objects.get_or_create(  # type: ignore
        name="Starfleet",
        slug="starfleet",
        group=TenantGroup.objects.get_or_create(name="Federation", slug="federation")[0],
    )[0]
    ip.dns_name = dns_name
    ip.tags.add("Tag1")
    ip.tags.add("Tag 2")
    return ip

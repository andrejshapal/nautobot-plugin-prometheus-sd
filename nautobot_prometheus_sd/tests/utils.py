"""Utility functions for Nautobot Prometheus SD tests."""

from django.db import IntegrityError
from nautobot.dcim.models import Device, Location, LocationType, Platform
from nautobot.dcim.models.devices import DeviceType, Manufacturer
from nautobot.extras.models import Role, Status
from nautobot.ipam.models import IPAddress, Namespace, Prefix
from nautobot.tenancy.models import Tenant, TenantGroup
from nautobot.virtualization.models import (
    Cluster,
    ClusterGroup,
    ClusterType,
    VirtualMachine,
)


def namespace():
    """Return the Global namespace."""
    obj, _ = Namespace.objects.get_or_create(
        name="Global", defaults={"description": "Default Global namespace. Created by Nautobot."}
    )
    return obj


def location_type():
    """Build a location type object for testing purposes."""
    return LocationType.objects.get_or_create(name="Building")[0]


def build_cluster():
    """Build a cluster object for testing purposes."""
    return Cluster.objects.get_or_create(
        name="DC1",
        cluster_group=ClusterGroup.objects.get_or_create(name="VMware")[0],
        cluster_type=ClusterType.objects.get_or_create(name="On Prem")[0],
        location=Location.objects.get_or_create(name="Campus A", location_type=location_type(), status=build_status())[
            0
        ],
    )[0]


def build_address(address):
    """Build an IP address object for testing purposes."""
    try:
        _ = Prefix.objects.get_or_create(prefix=address, status=build_status(), namespace=namespace())[0]
    except IntegrityError:
        pass
    return IPAddress.objects.get_or_create(address=address, status=build_status())[0]  # type: ignore


def build_tenant():
    """Build a tenant object for testing purposes."""
    return Tenant.objects.get_or_create(name="Acme Corp.")[0]


def build_status():
    """Build a status object for testing purposes."""
    return Status.objects.get_or_create(
        name="Active",
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
    vm.role = Role.objects.get_or_create(name="VM")[0]  # type: ignore
    vm.platform = Platform.objects.get_or_create(  # type: ignore
        name="Ubuntu 20.04"
    )[0]

    vm.primary_ip4 = build_address("192.168.0.1/24")  # type: ignore
    vm.primary_ip6 = build_address("2001:db8:1701::2/64")  # type: ignore

    vm.tags.add("Tag1")
    vm.tags.add("Tag 2")
    return vm


def build_minimal_device(name):
    """Build a minimal device object for testing purposes."""
    return Device.objects.get_or_create(
        name=name,
        status=build_status(),
        role=Role.objects.get_or_create(name="Firewall")[0],
        device_type=DeviceType.objects.get_or_create(
            model="SRX",
            manufacturer=Manufacturer.objects.get_or_create(
                name="Juniper",
            )[0],
        )[0],
        location=Location.objects.get_or_create(name="Site", location_type=location_type(), status=build_status())[0],
    )[0]


def build_device_full(name):
    """Build a full device object for testing purposes."""
    device = build_minimal_device(name)
    device.tenant = build_tenant()  # type: ignore
    device.status = build_status()
    device._custom_field_data = build_custom_fields()  # type: ignore # pylint: disable=protected-access
    device.platform = Platform.objects.get_or_create(name="Junos")[0]  # type: ignore

    device.primary_ip4 = build_address("192.168.0.1/24")  # type: ignore
    device.primary_ip6 = build_address("2001:db8:1701::2/64")  # type: ignore

    device.tags.add("Tag 2")
    return device


def build_full_ip(address, dns_name=""):
    """Build a full IP address object for testing purposes."""
    ip = build_address(address=address)  # pylint: disable=invalid-name
    ip.status = build_status()
    ip._custom_field_data = build_custom_fields()  # type: ignore # pylint: disable=protected-access
    ip.tenant = Tenant.objects.get_or_create(  # type: ignore
        name="Starfleet",
        tenant_group=TenantGroup.objects.get_or_create(name="Federation")[0],
    )[0]
    ip.dns_name = dns_name
    ip.tags.add("Tag1")
    ip.tags.add("Tag 2")
    return ip

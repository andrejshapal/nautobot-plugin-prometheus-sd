"""Tests for the Prometheus SD serializers."""

from django.test import TestCase

from ..api.serializers import (
    PrometheusDeviceSerializer,
    PrometheusIPAddressSerializer,
    PrometheusVirtualMachineSerializer,
)
from . import utils


class PrometheusVirtualMachineSerializerTests(TestCase):
    """Tests for the PrometheusVirtualMachineSerializer."""

    def test_vm_minimal_to_target(self):
        data = PrometheusVirtualMachineSerializer(instance=utils.build_minimal_vm("vm-01.example.com")).data

        self.assertEqual(data["targets"], ["vm-01.example.com"])
        for expected in [
            {"__meta_nautobot_model": "VirtualMachine"},
            {"__meta_nautobot_status": "Active"},
            {"__meta_nautobot_cluster": "DC1"},
            {"__meta_nautobot_cluster_group": "VMware"},
            {"__meta_nautobot_cluster_type": "On Prem"},
        ]:
            for k, v in expected.items():  # pylint: disable=invalid-name
                self.assertEqual(data["labels"].get(k), v)

    def test_vm_full_to_target(self):
        data = PrometheusVirtualMachineSerializer(instance=utils.build_vm_full("vm-full-01.example.com")).data

        self.assertEqual(data["targets"], ["vm-full-01.example.com"])
        for expected in [
            {"__meta_nautobot_model": "VirtualMachine"},
            {"__meta_nautobot_status": "Active"},
            {"__meta_nautobot_tenant": "Acme Corp."},
            {"__meta_nautobot_location": "Campus A"},
            {"__meta_nautobot_role": "VM"},
            {"__meta_nautobot_platform": "Ubuntu 20.04"},
            {"__meta_nautobot_primary_ip": "2001:db8:1701::2"},
            {"__meta_nautobot_primary_ip4": "192.168.0.1"},
            {"__meta_nautobot_primary_ip6": "2001:db8:1701::2"},
            {"__meta_nautobot_custom_field_simple": "Foobar 123"},
            {"__meta_nautobot_custom_field_int": "42"},
            {"__meta_nautobot_custom_field_bool": "True"},
            {"__meta_nautobot_custom_field_json": "{'foo': ['bar', 'baz']}"},
            {"__meta_nautobot_custom_field_multi_selection": "['foo', 'baz']"},
            {
                "__meta_nautobot_custom_field_contact": "[{'id': 1, 'url': 'http://localhost:8000/api/tenancy/contacts/1/', 'display': 'Foo', 'name': 'Foo'}]"
            },
            {"__meta_nautobot_custom_field_text_long": "This is\r\na  pretty\r\nlog\r\nText"},
        ]:
            for k, v in expected.items():  # pylint: disable=invalid-name
                self.assertEqual(data["labels"].get(k), v)


class PrometheusDeviceSerializerTests(TestCase):
    """Tests for the PrometheusDeviceSerializer."""

    def test_device_minimal_to_target(self):
        data = PrometheusDeviceSerializer(instance=utils.build_minimal_device("firewall-01")).data

        self.assertEqual(data["targets"], ["firewall-01"])
        for expected in [
            {"__meta_nautobot_model": "Device"},
            {"__meta_nautobot_role": "Firewall"},
            {"__meta_nautobot_device_type": "SRX"},
            {"__meta_nautobot_location": "Site"},
        ]:
            for k, v in expected.items():  # pylint: disable=invalid-name
                self.assertEqual(data["labels"].get(k), v)

    def test_device_full_to_target(self):
        data = PrometheusDeviceSerializer(instance=utils.build_device_full("firewall-full-01")).data

        self.assertEqual(data["targets"], ["firewall-full-01"])
        for expected in [
            {"__meta_nautobot_model": "Device"},
            {"__meta_nautobot_platform": "Junos"},
            {"__meta_nautobot_primary_ip": "2001:db8:1701::2"},
            {"__meta_nautobot_primary_ip4": "192.168.0.1"},
            {"__meta_nautobot_primary_ip6": "2001:db8:1701::2"},
            {"__meta_nautobot_tenant": "Acme Corp."},
            {"__meta_nautobot_custom_field_simple": "Foobar 123"},
        ]:
            for k, v in expected.items():  # pylint: disable=invalid-name
                self.assertEqual(data["labels"].get(k), v)


class PrometheusIPAddressSerializerTests(TestCase):
    """Tests for the PrometheusIPAddressSerializer."""

    def test_ip_minimal_to_target(self):
        data = PrometheusIPAddressSerializer(instance=utils.build_address("10.10.10.10/24")).data

        self.assertEqual(data["targets"], ["10.10.10.10"])
        for expected in [
            {"__meta_nautobot_status": "Active"},
            {"__meta_nautobot_model": "IPAddress"},
        ]:
            for k, v in expected.items():  # pylint: disable=invalid-name
                self.assertEqual(data["labels"].get(k), v)

    def test_ip_full_to_target(self):
        data = PrometheusIPAddressSerializer(
            instance=utils.build_full_ip(address="10.10.10.10/24", dns_name="foo.example.com")
        ).data

        self.assertEqual(
            data["targets"],
            ["foo.example.com"],
            "IP with DNS name should use DNS name as target",
        )
        for expected in [
            {"__meta_nautobot_status": "Active"},
            {"__meta_nautobot_model": "IPAddress"},
            {"__meta_nautobot_ip": "10.10.10.10"},
            {"__meta_nautobot_tenant": "Starfleet"},
            {"__meta_nautobot_tenant_group": "Federation"},
            {"__meta_nautobot_custom_field_simple": "Foobar 123"},
        ]:
            for k, v in expected.items():  # pylint: disable=invalid-name
                self.assertEqual(data["labels"].get(k), v)

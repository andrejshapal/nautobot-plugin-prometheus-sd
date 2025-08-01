"""FilterSet for Nautobot Prometheus Service Discovery."""

from nautobot.dcim.filters import DeviceFilterSet


class DeviceFilterSetCustom(DeviceFilterSet):
    """https://github.com/nautobot/nautobot/issues/7629!"""

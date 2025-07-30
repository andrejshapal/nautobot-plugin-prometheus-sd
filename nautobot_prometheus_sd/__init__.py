"""Nautobot plugin configuration for Prometheus Service Discovery (SD)."""

from nautobot.extras.plugins import PluginConfig


class PrometheusSD(PluginConfig):
    """Plugin configuration for Nautobot Prometheus SD."""

    name = "nautobot_prometheus_sd"
    verbose_name = "Nautobox Prometheus SD"
    description = (
        "Provide Prometheus url_sd compatible API Endpoint with data from netbox, based on nautobot_prometheus_sd"
    )
    version = "0.4"
    author = "Felix Peters"
    author_email = "mail@felixpeters.de"
    base_url = "prometheus-sd"
    required_settings = []
    default_settings = {}


config = PrometheusSD  # pylint:disable=invalid-name

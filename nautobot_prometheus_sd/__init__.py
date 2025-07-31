"""Nautobot plugin configuration for Prometheus Service Discovery (SD)."""

from nautobot.extras.plugins import NautobotAppConfig


class PrometheusSD(NautobotAppConfig):
    """Plugin configuration for Nautobot Prometheus SD."""

    name = "nautobot_prometheus_sd"
    verbose_name = "Nautobot Prometheus SD"
    description = (
        "Provide Prometheus url_sd compatible API Endpoint with data from netbox, based on nautobot_prometheus_sd"
    )
    version = "2.4.0"
    author = "Felix Peters"
    author_email = "mail@felixpeters.de"
    base_url = "prometheus-sd"
    required_settings = []
    default_settings = {}


config = PrometheusSD  # pylint:disable=invalid-name

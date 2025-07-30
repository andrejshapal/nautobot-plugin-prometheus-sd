I have found the following plugin: https://pypi.org/project/nautobot-plugin-prometheus-sd/ which is fork of https://github.com/FlxPeters/netbox-plugin-prometheus-sd, but without available source code, so copied the code to new repo, fixed the plugin for nautobot v1.6 and fixed tests. The most of the codebase belongs to user dubcl and Felix Peters.

# nautobot-plugin-prometheus-sd

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/FlxPeters/netbox-plugin-prometheus-sd/workflows/CI/badge.svg?event=push)](https://github.com/FlxPeters/netbox-plugin-prometheus-sd/actions?query=workflow%3ACI)
[![PyPI](https://img.shields.io/pypi/v/netbox-plugin-prometheus-sd)](https://pypi.org/project/netbox-plugin-prometheus-sd/)

Provide Prometheus http_sd compatible API Endpoint with data from Nautobot.

HTTP SD is a new feature in Prometheus 2.28.0 that allows hosts to be found via a URL instead of just files.
This plugin implements API endpoints in Nautobot to make devices, IPs and virtual machines available to Prometheus.

## Compatibility

For now we Support Nautobot `1.6`.
All relevant target versions are tested in CI. Have a look at the Github Actions definition for the current build targets.

## Installation

Generic guide how to work with plugins can be found in Nautobot documentation: https://docs.nautobot.com/projects/core/en/v1.6.23/plugins/#installing-plugins

1. `pip install nautobot-plugin-prometheus-sd` or add `nautobot-plugin-prometheus-sd` in `local_requirements.txt` of Nautobot.
2. In Nautobot configuration add:
```
PLUGINS = ['nautobot_prometheus_sd']
```

## Usage

The plugin only provides a new API endpoint on the Nautobot API. There is no further action required after installation.

### API

The plugin reuses Nautobot API view sets with new serializers for Prometheus.
This means that all filters that can be used on the Netbox api can also be used to filter Prometheus targets.
Paging is disabled because Prometheus does not support paged results.

The plugin also reuses the Nautobot authentication and permission model.
Depending on the Nautobot configuration, a token with valid object permissions must be passed to Nautobot.

```
GET        /api/plugins/prometheus-sd/devices/              Get a list of devices in a prometheus compatible format
GET        /api/plugins/prometheus-sd/virtual-machines/     Get a list of vms in a prometheus compatible format
GET        /api/plugins/prometheus-sd/ip-addresses/         Get a list of ip in a prometheus compatible format
```

### Example

After Plugin is installed in Nautobot, the prometheus can start to retrieve endpoints for scrapping using the following scrape config:
```
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ["localhost:9090"]
       # The label name is added as a label `label_name=<label_value>` to any timeseries scraped from this config.
        labels:
          app: "prometheus"
  - job_name: "sql_exporter"
    http_sd_configs:
        - url: http://10.248.113.8:8080/api/plugins/prometheus-sd/virtual-machines?status=active&tag=psql
          refresh_interval: 15s
          authorization:
            type: "Token"
            credentials: "LcQ27bHXgrd0TKIfJ3LchLFsOkVkK38TWa6uYuuh"
    relabel_configs:
      # Labels which control scraping
      - source_labels: [__meta_netbox_name]
        target_label: instance
      - source_labels: [__meta_netbox_primary_ip4]
        regex: '(.+)'
        target_label: __address__
      - source_labels: [__address__]
        target_label: __address__
        replacement: '${1}:9399'
      # Optional extra metadata labels
      - target_label: 'exp_type'
        replacement: 'pg'
      - target_label: 'cluster_name'
        replacement: 'crunchy'
```
In the config above, we are retrieving lists of lists of key value pairs. Every list of kv pairs is transformed using `relabel_configs` in order to provide `__address__` for the prometheus to scrape from. Additionally we are adding some static labels to the scraped targets. Excesive labels can be dropped.

## Development

Generic guide how to develope plugin can be found in Nautobot documentation: https://docs.nautobot.com/projects/core/en/v1.6.18/plugins/development/

Currently, we do not have well automated way of plugin development environment.

1. Install nautobot according to: https://docs.nautobot.com/projects/core/en/stable/user-guide/administration/installation/nautobot/
2. Clone this repository to the local machine.
3. The plugin should be installed in the same venv where Nautobot is running. Usually `source /opt/nautobot/bin/activate` (but could differ if you installed venv in different location).
4. Install plugin with `poetry install` (poetry should be installed already).

Visit http://localhost:8000 and log in with the new user.
You can now define Netbox entities and test around.

API endpoints for testing can be found at http://localhost:8000/api/plugins/prometheus-sd/

For tests the following command can be used:
`nautobot-server test .`

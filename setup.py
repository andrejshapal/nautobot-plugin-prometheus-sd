# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_prometheus_sd',
 'nautobot_prometheus_sd.api',
 'nautobot_prometheus_sd.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nautobot-plugin-prometheus-sd',
    'version': '0.0.1',
    'description': 'A Netbox plugin to provide Netbox entires to Prometheus HTTP service discovery',
    'long_description': "# fork to try this plugin nautobot compatible\n\n# netbox-plugin-prometheus-sd\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![CI](https://github.com/FlxPeters/netbox-plugin-prometheus-sd/workflows/CI/badge.svg?event=push)](https://github.com/FlxPeters/netbox-plugin-prometheus-sd/actions?query=workflow%3ACI)\n[![PyPI](https://img.shields.io/pypi/v/netbox-plugin-prometheus-sd)](https://pypi.org/project/netbox-plugin-prometheus-sd/)\n\nProvide Prometheus http_sd compatible API Endpoint with data from Netbox.\n\nHTTP SD is a new feature in Prometheus 2.28.0 that allows hosts to be found via a URL instead of just files.\nThis plugin implements API endpoints in Netbox to make devices, IPs and virtual machines available to Prometheus.\n\n## Compatibility\n\nWe aim to support the latest major versions of Netbox. For now we Support Netbox `2.11`, `3.0`, `3.1`, `3.2` and `3.3` including bugfix versions.\nAll relevant target versions are tested in CI. Have a look at the Github Actions definition for the current build targets.\n\n## Installation\n\nThe plugin is available as a Python package in pypi and can be installed with pip\n\n    pip install netbox-plugin-prometheus-sd\n\nEnable the plugin in /opt/netbox/netbox/netbox/configuration.py:\n\n    PLUGINS = ['netbox_prometheus_sd']\n\nThe plugin has not further plugin configuration at the moment.\n\n## Usage\n\nThe plugin only provides a new API endpoint on the Netbox API. There is no further action required after installation.\n\n### API\n\nThe plugin reuses Netbox API view sets with new serializers for Prometheus.\nThis means that all filters that can be used on the Netbox api can also be used to filter Prometheus targets.\nPaging is disabled because Prometheus does not support paged results.\n\nThe plugin also reuses the Netbox authentication and permission model.\nDepending on the Netbox configuration, a token with valid object permissions must be passed to Netbox.\n\n```\nGET        /api/plugins/prometheus-sd/devices/              Get a list of devices in a prometheus compatible format\nGET        /api/plugins/prometheus-sd/virtual-machines/     Get a list of vms in a prometheus compatible format\nGET        /api/plugins/prometheus-sd/ip-addresses/         Get a list of ip in a prometheus compatible format\n```\n\n### Example\n\nA working example on how to use this plugin with Prometheus is located at the `example` folder. Netbox content is created by using Netbox docker initializers.\n\nThe demo data doesn't make sense, but they are good enough for demonstrating how to configure Prometheus and get demo data to Prometheus service discovery.\n\nGo to the `example` folder and run `docker-compose up`. Prometheus should get available on `http://localhost:9090`. Netbox content should then be available in the service discovery tab.\n\n## Development\n\nWe use Poetry for dependency management and invoke as task runner.\nAs Netbox plugins cannot be tested standalone, we need invoke to start all code embedded in Netbox Docker containers.\n\nAll code to run in docker is located under `development`.\nTo start a virtual env managed by poetry run `poetry shell`.\nAll following commands are started inside this environment.\n\nIn order to run tests invoke the test steps\n\n``` bash\n# Execute all tests\ninvoke tests\n\n# Execute unit tests only\ninvoke unittest\n```\n\nFeatures should be covered by a unit test, but some times it's easier to develop on an running system.\n\n``` bash\n# Start a local Netbox with docker\ninvoke start\n\n# Create an user named `admin`\ninvoke create-user\n```\n\nVisit http://localhost:8000 and log in with the new user.\nYou can now define Netbox entities and test around.\n\nAPI endpoints for testing can be found at http://localhost:8000/api/plugins/prometheus-sd/\n",
    'author': 'Felix Peters',
    'author_email': 'felix.peters@breuninger.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

"""Nautobot Prometheus Service Discovery Setup Script."""
# -*- coding: utf-8 -*-
import os
from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

packages = \
['nautobot_prometheus_sd',
 'nautobot_prometheus_sd.api',
 'nautobot_prometheus_sd.tests']

package_data = \
{'': ['*']}

def get_version():
    """Get the version of the package."""
    return os.getenv('PACKAGE_VERSION', '1.6.1')

setup_kwargs = {
    'name': 'nautobot-plugin-prometheus-sd',
    'version': get_version(),
    'description': 'A Nautobot plugin to provide Netbox entires to Prometheus HTTP service discovery',
    'long_description': long_description,
    'long_description_content_type': 'text/markdown',
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

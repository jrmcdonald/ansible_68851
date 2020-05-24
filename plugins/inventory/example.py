from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
    name: example
    plugin_type: inventory
    author:
      - Jamie McDonald
    short_description: Ansible dynamic inventory plugin for demonstrating issue 68851.
    requirements:
        - python >= 2.7
    description:
        - Uses a YAML configuration file that ends with example.(yml|yaml).
    extends_documentation_fragment:
        - constructed
    options:
        plugin:
            description: marks this as an instance of the "example" plugin
            required: true
            choices: ["example"]
'''

from ansible.plugins.inventory import BaseInventoryPlugin, Constructable


class InventoryModule(BaseInventoryPlugin, Constructable):
    NAME = 'example'

    def verify_file(self, path):
        return (
                super(InventoryModule, self).verify_file(path) and
                path.endswith(("example.yaml", "example.yml"))
        )

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)

        strict = self.get_option('strict')

        self.inventory.add_host("master-1")
        self.inventory.set_variable("master-1", "name", "master-1")
        self._set_composite_vars(self.get_option('compose'), self.inventory.get_host("master-1").get_vars(), "master-1", strict=strict)
        self._add_host_to_composed_groups(self.get_option('groups'), {}, "master-1", strict=strict)
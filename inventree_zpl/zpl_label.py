"""
inventree_zpl.zpl_label
ZPL Label Plugin class

@author Jacob Hipps <jacob@ycnrg.org>
@license MIT

https://ycnrg.org/
https://0int.io/

"""

import socket

from jinja2 import Template
from django.utils.translation import ugettext_lazy as _

from plugin import InvenTreePlugin
from plugin.mixins import LabelPrintingMixin, SettingsMixin


class ZPLLabelPlugin(LabelPrintingMixin, SettingsMixin, InvenTreePlugin):

    AUTHOR = "Jacob Hipps <jacob@ycnrg.org>"
    DESCRIPTION = "ZPL Label Plugin"
    VERSION = "0.1.0"
    NAME = "ZPL"
    SLUG = "zpl"
    TITLE = "ZPL Label Printer"

    SETTINGS = {
        'HOSTNAME': {
            'name': _('Hostname'),
            'description': _('Printer hostname or IP address'),
            'default': '',
        },
        'PORT': {
            'name': _('Port'),
            'description': _('ZPL network port'),
            'default': '9100',
        },
        'TIMEOUT': {
            'name': _('Timeout'),
            'description': _('Network TCP timeout'),
            'default': 15,
        },
        'TEMPLATE_PATH': {
            'name': _('Template Path'),
            'description': _('ZPL Jinja2 template file path'),
            'default': '/home/inventree/data/example_2x1.j2',
        },
    }

    def print_label(self, **kwargs):

        # Get settings
        zpl_host = self.get_setting('HOSTNAME')

        try:
            zpl_port = int(self.get_setting('PORT'))
        except:
            zpl_port = 9100
            print("ZPL: WARNING: PORT config option is invalid; defaulting to 9100")

        try:
            zpl_timeout = int(self.get_setting('TIMEOUT'))
        except:
            zpl_timeout = 15
            print("ZPL: WARNING: TIMEOUT config option is invalid; defaulting to 15")

        templ_path = self.get_setting('TEMPLATE_PATH')

        object_to_print = kwargs['label_instance'].object_to_print

        if kwargs['label_instance'].SUBDIR == 'part':
            tpart = object_to_print
        elif kwargs['label_instance'].SUBDIR == 'stockitem':
            tpart = object_to_print.part
        else:
            print(f"!! Unsupported item type: {object_to_print.SUBDIR}")
            return

        try:
            with open(templ_path) as f:
                template = Template(f.read())
        except Exception as e:
            print(f"ZPL: ERROR: failed to read template from file: {templ_path}")
            raise(e)

        fields = {
            'name': tpart.name,
            'description': tpart.description,
            'ipn': tpart.IPN,
            'pk': tpart.pk,
            'params': tpart.parameters_map(),
            'category': tpart.category.name,
            'category_path': tpart.category.pathstring
        }

        # Give template access to the full part object + preprocessed fields
        raw_zpl = template.render(part=tpart, **fields).encode('utf-8')

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(zpl_timeout)
            sock.connect((zpl_host, zpl_port))
            sock.send(raw_zpl)
        except Exception as e:
            print(f"ZPL: ERROR: Failed to connect to host {zpl_host}:{zpl_port}")
            raise(e)

        sock.close()
        print("ZPL: Spooled label to printer {zpl_host} successfully")


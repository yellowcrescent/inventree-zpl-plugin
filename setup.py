from setuptools import setup, find_packages

setup(
    name = "inventree-zpl-plugin",
    version = "0.1.0",
    author = "Jacob Hipps",
    author_email = "jacob@ycnrg.org",
    license = "MIT",
    description = "ZPL label plugin for InvenTree",
    keywords = "inventree zpl label plugin",
    url = "https://ycnrg.org/",

    packages = find_packages(),
    scripts = [],

    install_requires = ['jinja2'],

    entry_points = {
        'inventree_plugins': [ 'ZPLLabelPlugin = inventree_zpl.zpl_label:ZPLLabelPlugin' ]
    }

)

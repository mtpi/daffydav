from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='DaffyDav',
      version=version,
      description="General purpose fileserver supporting WebDAV and HTTP protocols (providing web-based file manager)",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Matteo Pillon',
      author_email='matteo.pillon@gmail.com',
      url='',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'Paste',
          'PasteDeploy',
          'PasteScript',
          'fs',
          'WebOB',
          'Mako',
          'simplejson',
      ],
      entry_points={
        'paste.app_factory': ['main = daffydav.factories:make_app'],
        },
      )

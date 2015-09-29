from __future__ import print_function
import os

from setuptools import setup, find_packages

try:
    from gi.repository import Gtk, Gdk, GLib
    from gi.repository import AppIndicator3
    from gi.repository import Notify
except ImportError:
    packages = ('gir1.2-appindicator3', 'python-appindicator',
                'gir1.2-gtk-2.0', 'gir1.2-gtk-3.0', 'gir1.2-glib-2.0',
                'gir1.2-appindicator3-0.1', 'gir1.2-notify-0.7')
    print('You have to install "%s"' % ('", "'.join(packages)))
    raise


here = os.path.abspath(os.path.dirname(__file__))
name = 'totp.widget'

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.md')) as f:
    CHANGES = f.read()


requires = ['gnupg']

extras_require = {
    'dev': [],
    'test': ['nose'],
}

tests_requires = requires + extras_require['test']


setup(name=name,
      version='0.1',
      description='Widget to get totp token.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
      ],
      author='',
      author_email='',
      url='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_requires,
      entry_points="""\
[console_scripts]
wtotp = wtotp.__main__:main
      """,
      package_data = {
          'totp.widget': ['resources/*.png'],
      }
)


#!/usr/bin/env python

import argparse
import gnupg
import os
import subprocess
import sys

from getpass import getpass

from gi.repository import Gtk, Gdk
from gi.repository import AppIndicator3 as appindicator

CURR_DIR = os.path.split(__file__)[0]


class TotpWidget(object):

    def __init__(self):
        self.indicator = appindicator.Indicator.new(
            "totp.widget",
            "totp.widget",
            appindicator.IndicatorCategory.APPLICATION_STATUS)

        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        icon = os.path.join(CURR_DIR, 'resources', 'totp.png')
        self.indicator.set_icon(icon)

        self.menu = Gtk.Menu()

        item = Gtk.ImageMenuItem.new_with_label('TOTP')
        item.set_always_show_image(True)
        item.connect('activate', self.get_totp_value)
        item.show()
        self.menu.append(item)

        item = Gtk.ImageMenuItem.new_with_label('Quit')
        item.set_always_show_image(True)
        item.connect('activate', self.on_exit_activate)
        item.show()
        self.menu.append(item)

        self.menu.show()
        self.indicator.set_menu(self.menu)

        homedir = os.path.join(os.environ['HOME'], '.gnupg')

        parser = argparse.ArgumentParser(description='TOTP widget.')
        parser.add_argument('--gpg-dir', dest='homedir',
                            default=homedir, help='Path to the gpg dir.')
        parser.add_argument('--vault', dest='vault',
                            help='Where the totp seed is stored.')

        kwargs, _ = parser.parse_known_args(sys.argv[1:])

        gpg = gnupg.GPG(homedir=kwargs.homedir, verbose=True)

        with open(kwargs.vault) as fhandle:
            data = fhandle.read()

        password = getpass()

        decrypt = gpg.decrypt(data, passphrase=password)
        self.totp_token = decrypt.data.strip().split('\n')[-1]

    def copy(self, _, element):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(element, -1)

    def on_exit_activate(self, widget):
        self.on_destroy(widget)

    def on_destroy(self, _, data=None):
        Gtk.main_quit()

    def get_totp_value(self, widget):
        cmd = '/usr/bin/oathtool --base32 --totp %s' % self.totp_token
        value = subprocess.check_output(cmd.split(' '))
        self.copy(widget, str(value))


if __name__ == "__main__":
    # create the widget menu
    TotpWidget()


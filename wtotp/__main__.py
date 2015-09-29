#!/usr/bin/python
# -*- coding: utf-8 -*-

from wtotp import TotpWidget
from gi.repository import Gtk


def main():
    # create the widget menu
    TotpWidget()
    # run the widget
    Gtk.main()


if __name__ == "__main__":
    main()

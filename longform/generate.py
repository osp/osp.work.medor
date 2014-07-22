#! /usr/bin/env python2

import os
import sys
from django.conf import settings
from django.template import Context, loader
from optparse import OptionParser
from shutil import rmtree


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-c", "--clean", action="store_true", dest="clean", default=False, help="clean cache")

    (options, args) = parser.parse_args()

    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
    settings.configure(
        TEMPLATE_DIRS=(os.path.join(PROJECT_DIR, 'templates'),),
        INSTALLED_APPS=('mediawiki',),
        CACHE_PATH=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cache')
    )

    if options.clean:
        rmtree(settings.CACHE_PATH, True)

    t = loader.get_template('longform.html')
    c = Context({})

    sys.stdout.write(t.render(c).encode('utf-8'))

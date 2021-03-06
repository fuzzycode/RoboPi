# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Björn Larsson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ConfigParser
import logging
import os.path

__logger = logging.getLogger(__name__)

CONFIG = {
    "wheel_radius":5,
    "wheel_base":10,
    "fps":20
}

def init(files=list()):
    config = ConfigParser.SafeConfigParser(defaults=CONFIG)

    for f in config.read(['robopi.cfg', os.path.expanduser('~/.robopi.cfg')]):
        __logger.debug("Loaded config from {0}".format(f))

    try:
        CONFIG['wheel_radius'] = config.getfloat("physics", "wheel_radius")
        CONFIG['wheel_base'] = config.getfloat("physics", "wheel_base")
        CONFIG["fps"] = config.getint("operations", "fps")
    except ConfigParser.Error:
        __logger.warning("Error when loading configuration")
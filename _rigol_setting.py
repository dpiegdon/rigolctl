#
from __future__ import print_function

import collections
import time

Setting = collections.namedtuple('Setting', ['name', 'israw', 'value'])

def get_settings(instrument):
    wanted_settings = [ Setting('system:setup',     True,   None)
                    # this catches MOST settings, but not the below:
                    ,   Setting('math:fft:mode',    False,  None)
                    ,   Setting('math:fft:hscale',  False,  None)
                    ,   Setting('math:fft:hcenter', False,  None)
                    ]
    saved_settings = []

    for s in wanted_settings:
        print("saving {}".format(s.name))
        if s.israw:
            saved_settings.append(Setting(s.name, s.israw, instrument.ask_raw(':' + s.name + '?')))
        else:
            saved_settings.append(Setting(s.name, s.israw, instrument.ask(':' + s.name + '?')))

    return saved_settings

def set_settings(instrument, saved_settings):
    for s in saved_settings:
        print("restoring {}".format(s.name))
        if s.israw:
            instrument.write_raw(':' + s.name + ' ' + s.value)
        else:
            instrument.write(':' + s.name + ' ' + s.value)
        time.sleep(1)


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

class disabled_beeper(object):
    """ context which disables beeper for some piece of code
        
        with disabled_beeper(instrument):   << beeper is disabled
            some code
                                            << beeper is enabled
                                               if it was enabled before
        some more code
        """
    def __init__(self, instrument):
        self._instrument = instrument

    def __enter__(self):
        self._was_enabled = int(self._instrument.ask(":system:beeper?"))
        if self._was_enabled != 0:
            self._instrument.write(":system:beeper 0")

    def __exit__(self, typ, value, traceback):
        if self._was_enabled != 0:
            self._instrument.write(":system:beeper 1")

class locked_keyboard(object):
    """ context which completely locks the device keyboard:
        
        with locked_keyboard(instrument):   << keyboard is locked
            some code
                                            << keyboard is unlocked
                                               if it was unlocked before
        some more code
        """
    def __init__(self, instrument):
        self._instrument = instrument

    def __enter__(self):
        self._was_locked = int(self._instrument.ask(":system:locked?"))
        if self._was_locked != 1:
            self._instrument.write(":system:locked 1")

    def __exit__(self, typ, value, traceback):
        if self._was_locked != 1:
            self._instrument.write(":system:locked 0")

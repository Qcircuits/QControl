# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 17:42:11 2017

@author: Théau
"""

# -*- coding: utf-8 -*-
#==============================================================================
# module : agilent_multimeter.py
# author : Matthieu Dartiailh
# license : MIT license
#==============================================================================
"""
This module defines drivers for yokogawa sources using VISA library.

:Contains:
    Tenma : Driver for the Tenma 72-2535 using SERIAL

    BRICOLAGE!!!

"""
import re
import serial
from textwrap import fill
from inspect import cleandoc

from ..driver_tools import (InstrIOError, instrument_property,
                            secure_communication)
from ..visa_tools import VisaInstrument, VisaTypeError


class Tenma72_2535(VisaInstrument):
    """
    Driver for the Tenma72_2535, using the SERIAL library.

    This driver does not give access to all the functionnality of the
    instrument but you can extend it if needed. See the documentation of the
    `driver_tools` package for more details about writing instruments drivers.

    Parameters
    ----------


    Attributes
    ----------
    voltage : float, instrument_property
        Voltage at the output of the generator in volts.
    function : str, instrument_property
        Current function of the generator can be either 'VOLT' or 'CURR' (case
        insensitive).
    output : bool, instrument_property
        State of the output 'ON'(True)/'OFF'(False).

    """
    def __init__(self, connection_info, caching_allowed=True,
                 caching_permissions={}, auto_open=True):
        super(VisaInstrument, self).__init__(connection_info, caching_allowed,
                                             caching_permissions)
        if connection_info['additionnal_mode'] != '':
            self.connection_str =\
                str(connection_info['connection_type']
                    + '::' + connection_info['address']
                    + '::' + connection_info['additionnal_mode'])
        else:
            self.connection_str =\
                str(connection_info['connection_type']
                    + '::' + connection_info['address'])
        self._driver = None
        if auto_open:
            self.open_connection()

    def open_connection(self, **para):
        """Open the connection to the instr using the `connection_str`
        """
#        try:
        self._driver = serial.Serial(port='COM3', baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1, xonxoff=False, rtscts=False, write_timeout=None, dsrdtr=False, inter_byte_timeout=None)
        self._driver.write('BEEP1')
#        except VisaIOError as er:
#            self._driver = None
#            raise InstrIOError(str(er))



    @instrument_property
    @secure_communication()
    def voltage(self):
        """Voltage getter method. NB: does not check the current function.
        """
        self._driver.write("VSET1?")
        volt = self._driver.read(5)
        if volt is not None:
            return float(volt)
        else:
            raise InstrIOError('Instrument did not return the voltage')

    @voltage.setter
    @secure_communication()
    def voltage(self, set_point):
        """Voltage setter method. NB: does not check the current function.
        """
        val = "{:05.2f}".format(set_point)
        self._driver.write('VSET1:' + val)


    @instrument_property
    #@secure_communication()
    def function(self):
        """Function getter method
        """
        value = self.ask('SOURce:FUNCtion?')
        if value is not None:
            #Stripping leading and trailing '
            return value
        else:
            raise InstrIOError('Instrument did not return the function')

    @function.setter
    #@secure_communication()
    def function(self, mode):
        """Function setter method
        """
        volt = re.compile('VOLT', re.IGNORECASE)
        curr = re.compile('CURR', re.IGNORECASE)
        if volt.match(mode):
            self.write(':SOURce:FUNCtion VOLT')
            value = self.ask('SOURce:FUNCtion?')
            if value[1:-1] != 'VOLT':
                raise InstrIOError('Instrument did not set correctly the mode')
        elif curr.match(mode):
            self.write(':SOURce:FUNCtion CURR')
            value = self.ask('SOURce:FUNCtion?')
            if value[1:-1] != 'CURR':
                raise InstrIOError('Instrument did not set correctly the mode')
        else:
            mess = fill('''The invalid value {} was sent to set_function
                        method of the Yokogawa driver'''.format(value), 80)
            raise VisaTypeError(mess)


#    def check_connection(self):
#        """Found no way to check whether or not the cache can be corrupted
#        """
#        return False
#DRIVER_PACKAGES = ['serial']
#DRIVER_TYPES = {'Serial': Tenma72_2535}
DRIVERS = {'Tenma72_2535': Tenma72_2535}
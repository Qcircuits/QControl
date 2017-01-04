# -*- coding: utf-8 -*-
#==============================================================================
# module : r&s_fsv.py
# author : Benjamin Huard
# license : MIT license
#==============================================================================
"""
This module defines drivers for Rhode&Schwarz PSA.

:Contains:
    RandS_FSV

"""
from inspect import cleandoc
import numpy as np
from ..driver_tools import (InstrIOError, secure_communication,
                            instrument_property)
from ..visa_tools import VisaInstrument
import time

class RandS_FSV(VisaInstrument):
    """
    """
    caching_permissions = {'start_frequency_SA': False,
                           'stop_frequency_SA': False}

    def __init__(self, connection_info, caching_allowed=True,
                 caching_permissions={}, auto_open=True):
        super(RandS_FSV, self).__init__(connection_info,
                                         caching_allowed,
                                         caching_permissions,
                                         auto_open)
        self.mode = 'SA'
        self.write('*CLS')
        self.write('*SRE 168')
        self.write('*ESE 61')
        self.write('STAT:OPER:ENAB 0')
        self.write('STAT:QUES:ENAB 0')
        self.write("FORM:DATA ASCii")

    @secure_communication()
    def read_data(self, trace):
        """
        """

        self.write('SYST:DISP:UPD OFF')
        # turn the display off for better performances
        # go to the "Single sweep" mode
        self.write("INIT:CONT OFF")
        # stop all the measurements
        self.write("ABORT")
        # initiate measurement
        self.write("INIT;*WAI")

        while True:
            try:
                self.ask_for_values("SWEEP:TIME?")
                break
            except:
                pass

        data = self.ask_for_values('trace? trace{}'.format(trace))

        if data:
            freq = np.round(1e14*np.linspace(self.start_frequency_SA,
                               self.stop_frequency_SA,
                               self.sweep_points_SA))*1e-14
            return np.rec.fromarrays([freq, np.array(data)],
                                     names=['Frequency','data'])
        else:
            raise InstrIOError(cleandoc('''Rhode&Schwarz FSV did not return the
                trace {} data'''.format(trace)))

        self.write('SYST:DISP:UPD ON')


    @instrument_property
    @secure_communication()
    def start_frequency_SA(self):
        """Start frequency getter method

        """
        freq = self.ask_for_values('FREQ:STARt?')
        if freq:
            return freq[0]/1e9
        else:
            raise InstrIOError(cleandoc('''R&S PSA did not return the
                start frequency'''))

    @start_frequency_SA.setter
    @secure_communication()
    def start_frequency_SA(self, value):
        """Start frequency setter method
        """

        self.write('FREQ:STARt {} GHz'.format(value))
        result = self.ask_for_values('FREQ:STARt?')
        if result:
            if abs(result[0]/1e9 - value)/value > 10**-12:
                raise InstrIOError(cleandoc('''PSA did not set correctly
                the start frequency'''))
        else:
            raise InstrIOError(cleandoc('''PSA did not set correctly the
                start frequency'''))

    @instrument_property
    @secure_communication()
    def stop_frequency_SA(self):
        """Stop frequency getter method
        """

        freq = self.ask_for_values('FREQ:STOP?')
        if freq:
            return freq[0]/1e9
        else:
            raise InstrIOError(cleandoc('''Agilent PSA did not return the
                stop frequency'''))


    @stop_frequency_SA.setter
    @secure_communication()
    def stop_frequency_SA(self, value):
        """Stop frequency setter method

        """

        self.write('FREQ:STOP {} GHz'.format(value))
        result = self.ask_for_values('FREQ:STOP?')
        if result:
            if abs(result[0]/1e9 - value)/value > 10**-12:
                raise InstrIOError(cleandoc('''PSA did not set correctly
                the stop frequency'''))
        else:
            raise InstrIOError(cleandoc('''PSA did not set correctly the
                stop frequency'''))

    @instrument_property
    @secure_communication()
    def center_frequency(self):
        """Center frequency getter method

        """

        freq = self.ask_for_values('FREQ:CENT?')
        if freq:
            return freq[0]/1e9
        else:
            raise InstrIOError(cleandoc('''Agilent PSA did not return the
                    center frequency'''))

    @center_frequency.setter
    @secure_communication()
    def center_frequency(self, value):
        """center frequency setter method
        """

        self.write('FREQ:CENT {} GHz'.format(value))
        result = self.ask_for_values('FREQ:CENT?')
        if result:
            if abs(result[0]/1e9 - value)/value > 10**-12:
                raise InstrIOError(cleandoc('''PSA did not set correctly the
                    center frequency'''))
        else:
            raise InstrIOError(cleandoc('''PSA did not set correctly the
                    center frequency'''))

    @instrument_property
    @secure_communication()
    def span_frequency(self):
        """Span frequency getter method

        """
        freq = self.ask_for_values('FREQ:SPAN?')
        if freq:
            return freq[0]/1e9
        else:
            raise InstrIOError(cleandoc('''Agilent PSA did not return the
                span frequency'''))

    @span_frequency.setter
    @secure_communication()
    def span_frequency(self, value):
        """span frequency setter method
        """
        self.write('FREQ:SPAN {} GHz'.format(value))
        result = self.ask_for_values('FREQ:SPAN?')
        if result:
            if abs(result[0]/1e9 - value)/value > 10**-12:
                raise InstrIOError(cleandoc('''FSV did not set correctly
                the span frequency'''))
        else:
            raise InstrIOError(cleandoc('''FSV did not set correctly the
                span frequency'''))


    @instrument_property
    @secure_communication()
    def sweep_time(self):
        """Sweep time getter method
        """
        sweep = self.ask_for_values('SWEEP:TIME?')
        if sweep:
            return sweep[0]
        else:
            raise InstrIOError(cleandoc('''PSA did not return the
                sweep time'''))

    @sweep_time.setter
    @secure_communication()
    def sweep_time(self, value):
        """sweep time setter method
        """
        self.write('SWEEP:TIME {}'.format(value))
        result = self.ask_for_values('SWEEP:TIME?')
        if result:
            if abs(result[0] - value)/value > 10**-12:
                raise InstrIOError(cleandoc('''PSA did not set correctly
                the sweep time'''))
        else:
            raise InstrIOError(cleandoc('''PSA did not set correctly the
                sweep time'''))


    @instrument_property
    @secure_communication()
    def RBW(self):
        """
        """
        rbw = self.ask_for_values('band:res?')
        if rbw:
            return rbw[0]
        else:
            raise InstrIOError(cleandoc('''PSA did not return the
                RBW'''))


    @RBW.setter
    @secure_communication()
    def RBW(self, value):
        """
        """
        self.write('band:res {}'.format(value))
        result = self.ask_for_values('band:res?')
        if result:
            if abs(result[0] > value) > 10**-12:
                raise InstrIOError(cleandoc('''PSA did not set correctly
                the channel Resolution bandwidth'''))
        else:
            raise InstrIOError(cleandoc('''PSA did not set correctly the
                channel Resolution bandwidth'''))


    @instrument_property
    @secure_communication()
    def VBW_SA(self):
        """
        """
        vbw = self.ask_for_values('BAND:VID?')
        if vbw:
            return vbw[0]
        else:
            raise InstrIOError(cleandoc('''Agilent PSA did not return the
                channel Video bandwidth'''))

    @VBW_SA.setter
    @secure_communication()
    def VBW_SA(self, value):
        """
        """
        self.write('BAND:VID {}'.format(value))
        result = self.ask_for_values('BAND:VID?')
        if result:
            if abs(result[0] > value) > 10**-12:
                raise InstrIOError(cleandoc('''PSA did not set correctly
                the channel Video bandwidth'''))
        else:
            raise InstrIOError(cleandoc('''PSA did not set correctly the
                channel Video bandwidth'''))

    @instrument_property
    @secure_communication()
    def sweep_points_SA(self):
        """
        """
        points = self.ask_for_values('SWEep:POINts?')
        if points:
            return points[0]
        else:
            raise InstrIOError(cleandoc(''' PSA did not return the
                    sweep point number'''))

    @sweep_points_SA.setter
    @secure_communication()
    def sweep_points_SA(self, value):
        """
        """
        self.write('SWEep:POINts {}'.format(value))
        result = self.ask_for_values('SWEep:POINts?')
        if result:
            if result[0] != value:
                raise InstrIOError(cleandoc('''PSA did not set correctly the
                    sweep point number'''))
        else:
            raise InstrIOError(cleandoc('''PSA did not set correctly the
                    sweep point number'''))

    @instrument_property
    @secure_communication()
    def average_count_SA(self):
        """
        """
        count = self.ask_for_values('AVERage:COUNt?')
        if count:
            return count[0]
        else:
            raise InstrIOError(cleandoc('''Agilent PSA did not return the
                     average count'''))

    @average_count_SA.setter
    @secure_communication()
    def average_count_SA(self, value):
        """
        """
        self.write('AVERage:COUNt {}'.format(value))
        result = self.ask_for_values('AVERage:COUNt?')
        if result:
            if result[0] != value:
                raise InstrIOError(cleandoc('''PSA did not set correctly the
                     average count'''))
        else:
            raise InstrIOError(cleandoc('''PSA did not set correctly the
                     average count'''))

    @instrument_property
    @secure_communication()
    def average_state_SA(self):
        """
        """
        mode = self.ask('AVERage?')
        if mode:
            return mode
        else:
            raise InstrIOError(cleandoc('''Agilent PSA did not return the
                    average state'''))

    @average_state_SA.setter
    @secure_communication()
    def average_state_SA(self, value):
        """
        """
        self.write('AVERage:STATE {}'.format(value))
        result = self.ask('AVERage?')

        if result.lower() != value.lower()[:len(result)]:
            raise InstrIOError(cleandoc('''PSA did not set correctly the
                average state'''))


    @instrument_property
    @secure_communication()
    def marker_peak(self):
        """
        """        
        freq = self.ask_for_values('CALC:MARK:FUNC:FPE:X?')
        if freq:
            return float(freq[0])*1e-9
        else:
            raise InstrIOError(cleandoc('''FSV did not return a 
                                        peak position'''))



DRIVERS = {'RandS_FSV': RandS_FSV}

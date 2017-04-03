# -*- coding: utf-8 -*-
#==============================================================================
# module : formula_task.py
# author : Matthieu Dartiailh
# license : MIT license
#==============================================================================
"""
"""
from atom.api import (Enum, set_default)

from ..base_tasks import SimpleTask
import time

class GetDateTask(SimpleTask):
    """Get the date of the day with format mm/dd/yy or dd/mm/yy
    """
    #: List of formulas.
    dateformat = Enum('mm/dd/yy','dd/mm/yy').tag(pref=True)

    task_database_entries = set_default({'date': {}})

    def perform(self):
        """
        """
        value = self.dateformat
        value = value.replace('mm','m')
        value = value.replace('yy','y')
        value = value.replace('dd','d')
        value = value.replace('/','%')        
        value = '%' + value
        value = time.strftime(value)
        
        self.write_in_database('date', value)

    def check(self, *args, **kwargs):
        """
        """
        traceback = {}
        test = True
# 
        return test, traceback

KNOWN_PY_TASKS = [GetDateTask]

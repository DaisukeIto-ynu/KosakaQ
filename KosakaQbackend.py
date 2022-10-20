# -*- coding: utf-8 -*-


"""
Created on Thu Oct 20 16:47:43 2022

@author: Yokohama National University, Kosaka Lab
"""

from qiskit.providers import BackendV2
from qiskit.providers.jobstatus import JobStatus

from KosakaQ.KosakaQjob import KosakaQJob

class KosakaQbackend(BackendV2):
    def __init__(self, BACKEND):
        self.backend = BACKEND
        if BACKEND == "rabi":
            self.IP = "192.168.11.185"  # サーバーのローカルIP
            self.version = 2
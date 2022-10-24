# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 16:47:43 2022

@author: Yokohama National University, Kosaka Lab
"""

from abc import ABC
from abc import abstractmethod
import datetime
import logging
from typing import List, Union, Iterable, Tuple

from qiskit.providers.provider import Provider
from qiskit.providers.models.backendstatus import BackendStatus
from qiskit.circuit.gate import Instruction
from qiskit.providers import BackendV2
from qiskit.providers.jobstatus import JobStatus
from qiskit.transpiler.Target import Target
from qiskit.providers.options import Options
from qiskit.qobj.utils import MeasLevel, MeasReturnType

logger = logging.getLogger(__name__)

from KosakaQ.KosakaQjob import KosakaQJob
from KosakaQ.KosakaQcommunicate import KosakaQ_communicate


class KosakaQbackend(BackendV2):
    def __init__(self, BACKEND):
        self.backend = BACKEND
        if BACKEND == "rabi":
            self.IP = "192.168.11.185"  # サーバーのローカルIP
            self.version = 2
            
    
    def _check_run_input(run_input):
        """Return the qobj to be run on the backends.

        Args:
            run_input: argument of KosakaQbackend.run()

        Returns:
            Qobj: the qobj to be run on the backends
        """
        pass  # 雄真・優悟、この行を消してを消して書き加えてください！
    
   
    @property
    def target(self):
        """A :class:`qiskit.transpiler.Target` object for the backend.

        :rtype: Target
        """
        pass  # 翔・ひでよし、この行を消して`qiskit.transpiler.Target`というclassのオブジェクトをreturnしてください！propertyについてはOREILLY_入門_Python3_第2版_第Ⅰ部.pdfのp258を参照
    
    
    @classmethod
    def _default_options(cls) -> Options:
        """Default runtime options."""
        return Options(shots=4096, memory=False,
                       qubit_lo_freq=None, meas_lo_freq=None,
                       schedule_los=None,
                       meas_level=MeasLevel.CLASSIFIED,
                       meas_return=MeasReturnType.AVERAGE,
                       memory_slots=None, memory_slot_size=100,
                       rep_time=None, rep_delay=None,
                       init_qubits=True, use_measure_esp=None,
                       live_data_enabled=None)

   
    @property
    def max_circuits(self):
        """The maximum number of circuits (or Pulse schedules) that can be
        run in a single job.

        If there is no limit this will return None
        """
        return 1
    
    
    def run(self, run_input, **options):
        """Run on the backend.

        This method returns a :class:`~qiskit.providers.Job` object
        that runs circuits. Depending on the backend this may be either an async
        or sync call. It is at the discretion of the provider to decide whether
        running should block until the execution is finished or not: the Job
        class can handle either situation.

        Args:
            run_input (QuantumCircuit or Schedule or ScheduleBlock or list): An
                individual or a list of
                :class:`~qiskit.circuits.QuantumCircuit,
                :class:`~qiskit.pulse.ScheduleBlock`, or
                :class:`~qiskit.pulse.Schedule` objects to run on the backend.
            options: Any kwarg options to pass to the backend for running the
                config. If a key is also present in the options
                attribute/object then the expectation is that the value
                specified will be used instead of what's set in the options
                object.
        Returns:
            Job: The job object for the run
        """
        
        KQcom = KosakaQ_communicate(self._check_run_input(run_input), self.IP)
        
        ###job_id受付部分：サーバーからackが帰ってくるまで、lifeが残る限り例外処理を続け、timeoutする度に再送信する###
        send_uncomplete_life = 5
        while send_uncomplete_life>0:
            KQcom.send_jobid_query()
            try:
                KQcom.send_jobid_query()
            except:
                print("Connection failed: Retrying connetion\n")
                send_uncomplete_life -= 1
            else:
                try:
                    Job_id = KQcom.receive_job_id()
                    send_uncomplete_life = -1
                except:
                    print("Error: Unavailable job_id___connection error")
                    print("Retrying to send query\n")
                    send_uncomplete_life -= 1
        #lifeが尽きてwhile脱出してしまったらraise
        if send_uncomplete_life == 0:
            raise Exception('Error: Connection failed')
        ###job_id受付部分ここまで##############################################################
        
        ###送信部分：サーバーからackが帰ってくるまで、lifeが残る限り例外処理を続け、timeoutする度に再送信する###
        msg = -1
        send_uncomplete_life = 5
        while send_uncomplete_life>0:
            try:
                KQcom.send_file(Job_id)
            except:
                print("Connection failed: Retrying connetion\n")
                send_uncomplete_life -= 1
            else:
                #通信が確立した後、サーバーのackを待つ
                try:
                    msg = KQcom.receive_msg()
                except:
                    print("Error: Unavailable acception___connection error")
                    print("Retrying to send query\n")
                    send_uncomplete_life -= 1
                else:
                    if msg == 0:
                        print('Complete: query accepted!\n')
                        send_uncomplete_life = -1
                    else:
                        raise Exception('Error: Unavailable acception')
        #lifeが尽きてwhile脱出してしまったらraise
        if send_uncomplete_life == 0:
            raise Exception('Error: Connection failed')
        ###送信部分ここまで######################################################################
        
        ###受信部分###########################################################################
        KQcom.receive(Job_id.get("PORT"))
        ###受信部分ここまで######################################################################
        
        job = KosakaQJob(backend=self,job_id=Job_id.get("job_id"),PORT=Job_id.get("PORT"), _status = JobStatus.QUEUED)
        return job




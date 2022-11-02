# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 14:04:25 2022

@author: daisu
"""

# 必要なモジュールのimport
from qiskit import IBMQ, QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
import sys
sys.path.append(".")
from KosakaQbackend import KosakaQbackend
from qiskit.qasm import pi
from qiskit.tools.visualization import plot_histogram, circuit_drawer
import numpy as np
import time

backend = KosakaQbackend("rabi")


# 量子レジスタqを生成する。
q = QuantumRegister(1)

# 古典レジスタcを生成する
c = ClassicalRegister(1)

# 量子レジスタqを生成する。
q2 = QuantumRegister(1)

# 古典レジスタcを生成する
c2 = ClassicalRegister(1)

# 量子レジスタqを生成する。
q3 = QuantumRegister(1)

# 古典レジスタcを生成する
c3 = ClassicalRegister(1)


# 量子レジスタqと古典レジスタc間で量子回路を生成する。
qc = QuantumCircuit(q, c)
qc.i(q[0])
job = backend.run(qc)

# qc2 = QuantumCircuit(q2, c2)
# qc3 = QuantumCircuit(q3, c3)

# # 1番目の量子ビットにxゲートをかける。
# qc.h(q[0])
# qc.z(q[0])
# qc.h(q[0])

# qc2.h(q2[0])
# qc2.z(q2[0])
# qc2.h(q2[0])
# qc2.x(q2[0])

# qc3.sx(q3[0])
# qc3.s(q3[0])
# qc3.y(q3[0])
# qc3.s(q3[0])
# qc3.sx(q3[0])


# # 1番目の量子ビットの測定値を1番目の古典ビットに、2番目の量子ビットの測定値を2番目の古典ビットに渡す。
# qc.measure(q[0], c[0])
# qc2.measure(q2[0], c2[0])
# qc3.measure(q3[0], c3[0])


# # バックエンドで回路をshots回実行させ、測定結果を返させる
# job = []
# for i in range(2):
#     job.append(backend.run(qc))
#     job.append(backend.run(qc2))
#     job.append(backend.run(qc3))

# jobの監視
# from qiskit.tools.monitor import job_monitor
# job_monitor(job)

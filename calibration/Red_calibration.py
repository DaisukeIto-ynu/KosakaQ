# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 18:30:33 2022

@author: Yokohama National University, Kosaka Lab
"""


import copy
from qiskit.exceptions import KosakaQRedcalibrationError
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
 #グラフの描画のためのインポート
import sys
sys.path.append(".")
import matplotlib.pyplot as plt
import numpty as np
from exceptions.exceptions import RedCalibrationError
from KosakaQbackend import KosakaQbackend


class Red_calibration():
    def __init__(self):
        self.mode = None
        self.backend = KosakaQbackend("rabi")
        self.job_num = 0
        self.job = []
        self.mode = []
        self.calibration = []
    
    def run(self, mode):  # 大輔が作ります
        """
        mode: Ey or E1E2 or all
        どの周りのスペクトルを取るか選べる。
        """
        self.job.append(self.backend.run(mode))
        self.job_num += 1  # 発行したjobの数
        self.mode.append(mode)
        self.flag.append({})  # 各種Flag
        self.flag[-1]["get_result"] = False
        self.flag[-1]["calibration"] = False
        self.flag[-1]["fitting"] = False
        return self.job[-1]  # result[0]=frequencyのlist, result[1]=count（縦軸), result[2] = エラーバーのlist
    

    def jobs(self):
        if self.job_num == 0:
            print("There is no job.")
        else:
            for i in range(self.job_num):
                if self.flag[i]["get_result"] == False:
                    print("job",i+1,"... ","mode: ",self.mode[i], " get_result: not yet")
                else:
                    print("job",i+1,"... ","mode: ",self.mode[i], " get_result: done")
             
                
    def get_result(self, job_num = 0):  # job_num = 0にすることで、使うとき job_num-1 = -1 となり、最新のが使える。
        # self.flag[-1]["get_result"] = True　だったら、already executed表示
        if self.flag[-1]["get_result"] == True:
            print("Already executed")
        
        # job_status確認して表示
        nowstatus = self.job[job_num].status()
        if nowstatus == JobStatus.QUEUED: # status:queuedだったら、何番目か表示して、このまま待つか聞いて、待つようだったらjob monitor表示
            print("status : QUEUED")
            print("Now waiting")
        else nowstatus == JobStatus.VALIDATING:
            print("status : VALIDATING")
        else nowstatus == JobStatus.RUNNING:
            print("status : RUNNING")
        else nowstatus == JobStatus.CANCELLED:
            print("status : CANCELLED")
        else nowstatus == JobStatus.DONE: # status:doneだったら/なったら、result取ってくる。
            print("status : DONE")
        else nowstatus == JobStatus.ERROR:
            print("status : ERROR")
        
        
        # job_num > self.job_num or job_num < 0 or not( type(job_num) == int )　だったら、raiseする。
        # 最後に、self.flag[job_num-1]["get_result"] = True
        pass  # result[job_num-1][0]=frequencyのlist, result[job_num-1][1]=count（縦軸), result[job_num-1][2] = エラーバーのlist
    
    
    # author: Mori Yugo
    def draw(self, fitting=False, error=False, Ey=False, E1E2=False, save=False, job_num = 0):
        #get resultにデータがあるか
        
        # optionでfittingするか選べる ← fitingのlistには_make_fittingメソッドを使って下さい。
        if fitting == True:
            self._make_fitting(job_num)
        
        # optionでエラーバーいれるか選べる。
        if error == True:
            # exexute error bar
            pass
        
        # optionでE1E2,Eyの中心値を表示するか選べる。 ← 中心値にはcalibrationメソッドを使ってください。
        if Ey == True:
            self.calibration(job_num)
        if E1E2 == True:
            self.calibration(job_num)
            
        # optionで保存するか選べる。
        if save == True:
            pass
            # save
        
        # その他、optionを入れる。optionは引数にするが、あくまでoptionなので、選ばなくても良いようにする。
        
        # runをまだ実行してなかったら(self.mode == None)、エラーを返す。
        if self.mode == None:
            print("error: run function is not done.")   #exeptionsのエラーリストからエラー表示→ここも直す
        pass
    
    
    def laser_draw(self, fitting=False, Ey=False, E1E2=False, save=False, job_num = 0):
        # optionでfittingするか選べる ← fitingのlistはこちらは簡単だと思うので、自分で作って下さい。
        # optionで保存するか選べる。
        # その他、optionを入れる。optionは引数にするが、あくまでoptionなので、選ばなくても良いようにする。
        # runをまだ実行してなかったら(self.mode == None)、エラーを返す。
        pass

    # author: Honda Yuma
    def calibration(self, job_num = 0):  # E1E2とEyのキャリブレーション結果を返す ← E1E2は二つの頂点のちょうど中心を取る。Eyは_make_fittingのself.x0を返す。
        # runをまだ実行してなかったら(self.mode == None)、エラーを返す。
        # 結果は　self.calibration[job_num-1]に辞書で入れる。例）[{E1E2:470.0678453678},{E1E2:470.0034567, Ey:470.145678}]
        pass
    
    
    def save(self, job_num = 0):  # jsonにE1とExEy保存する。
        pass
    

    # author: Ebihara Syo
    def _make_fitting(self, job_num = 0):
        #E1,E2はエラーを返す
        #Eyについてのfitingのlistを返す（ローレンチアン）、x0とγをself.x0とself.gammaに代入
        #runをまだ実行してなかったら(self.mode == None)、エラーを返す。
        
        if self.mode == "E1":  # E1の場合
            raise KosakaQRedcalibrationError('E1です')
            
        elif self.mode == "E2":  # E2の場合
            raise KosakaQRedcalibrationError('E2です')
            
        elif self.mode == "Ey":  # Eyの場合
            fre_y = copy.deepcopy[self.result[job_num - 1][0]]  # 縦軸の値
            cou_x = copy.deepcopy[self.result[job_num - 1][1]]  # 横軸の値
            
            
            
            # Ey_frequencyはフィッティング後の縦軸の値
            Ey_frequency = 1
            return Ey_frequency
        
        elif self.mode == "All":  # 全体の場合
            return 0
        

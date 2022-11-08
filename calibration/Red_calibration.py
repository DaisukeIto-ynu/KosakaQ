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

class Red_calibration():
    def __init__(self):
        self.mode = None
        self.job_num = 0
        self.job = []
        self.mode = []
        self.calibration = []
    
    def run(self, mode):  # 大輔が作ります
        """
        mode: Ey or E1E2 or all
        どの周りのスペクトルを取るか選べる。
        """
        # self.result = []  # Rabi_project20_E6EL06_area06_NV04_PLE_all_0.txtの内容が入ったlistを返します。
        # self.power = []  #周波数 vs.laser_power
        self.job_num += 1  # 発行したjobの数
        self.mode.append(mode)
        self.flag.append({})  # 各種Flag
        self.flag[-1]["get_result"] = False
        self.flag[-1]["calibration"] = False
        self.flag[-1]["fitting"] = False
        return self.job[-1]  # result[0]=frequencyのlist, result[1]=count（縦軸), result[2] = エラーバーのlist
    

    # author: Goto Kyosuke
    def jobs(self):
        if self.job_num == 0:
            print("There is no job.")
        else:
            for i in range(self.job_num):
                if self.flag[i]["get_result"] == False:
                    print("job",i+1,"... ","mode: ",self.mode[i], " get_result: not yet")
                else:
                    print("job",i+1,"... ","mode: ",self.mode[i], " get_result: done")
             

    # author: Goto Kyosuke
    def get_result(self, job_num = 0):  # job_num = 0にすることで、使うとき job_num-1 = -1 となり、最新のが使える。
        # self.flag[-1]["get_result"] = True　だったら、already executed表示
        if self.flag[-1]["get_result"] == True:
            print("Already executed")
        
        # job_status確認して表示
        nowstatus = self.job[job_num].status()
        print(nowstatus.value)
        
        if nowstatus == JobStatus.QUEUED: # status:queuedだったら、何番目か表示して、このまま待つか聞いて、待つようだったらjob monitor表示
            print("You're job number is ",self.job[job_num].queue_position)
        
        elif nowstatus == JobStatus.DONE: # status:doneだったら/なったら、result取ってくる。
            #self.job[job_num] = 
        
        
        
        
        # job_num > self.job_num or job_num < 0 or not( type(job_num) == int )　だったら、raiseする。
        # 最後に、self.flag[job_num-1]["get_result"] = True
        pass  # result[job_num-1][0]=frequencyのlist, result[job_num-1][1]=count（縦軸), result[job_num-1][2] = エラーバーのlist
    
    
    # author: Mori Yugo
    def draw(self, fitting=False, error=0, Ey=False, E1E2=False, save=False, job_num = 0):
        """
        This function draws photoluminescence excitation (PLE).
        
        fitting: True or false
        フィッティングするか選ぶ
        
        error: 1, 2 or 3
        エラーバーを表示するか選ぶ
        
        Ey: True or false
        Eyの中心値を表示するか選ぶ
        
        E1E2: True or false
        E1E2の中心値を表示するか選ぶ
        
        save: True or false
        Ey, E1E2を保存するか選べる
        """
        #get resultにデータがあるか
        
        # optionでfittingするか選べる ← fitingのlistには_make_fittingメソッドを使って下さい。
        if fitting == True:
            self._make_fitting(job_num)
        
        # optionでエラーバーいれるか選べる。
        if error == 1
            # exexute error bar 1
            pass
        elif error = 2:
            # exexute error bar 2
            pass
        elif error = 3:
            # exexute error bar 3
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
            raise KosakaQRedcalibrationError("Run function is not done.")
    
    
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
        
        if self.mode == "E1_E2":  # E1_E2の場合
            raise KosakaQRedcalibrationError('E1_E2です')
            
        elif self.mode == "Ey":  # Eyの場合
            fre_y = copy.deepcopy[self.result[job_num - 1][0]]  # 縦軸の値
            cou_x = copy.deepcopy[self.result[job_num - 1][1]]  # 横軸の値
            
            
            
            # Ey_frequencyはフィッティング後の縦軸の値
            Ey_frequency = 1
            return Ey_frequency
        
        elif self.mode == "All":  # 全体の場合
            return 0
        

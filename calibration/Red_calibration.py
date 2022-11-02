# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 18:30:33 2022

@author: Yokohama National University, Kosaka Lab
"""

class Red_calibration():
    def __init__(self):
        self.mode = None
        self.job_num = 0
        self.mode = []
    
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
        return self.job[-1]  # result[0]=frequencyのlist, result[1]=count（縦軸), result[2] = エラーバーのlist
    
    def jobs(self):
        if self.job_num == 0:
            print("There is no job.")
        else:
            for i in range(self.job_num):
                print("job",i+1,"... ","mode:",self.mode[i], " get_result: not yet")
             
                
    def get_result(self, job_num = 0):  # job_num = 0にすることで、使うとき job_num-1 = -1 となり、最新のが使える。
        # self.flag[-1]["get_result"] = True　だったら、already executed表示
        # job_status確認して表示
        # status:queuedだったら、何番目か表示して、このまま待つか聞いて、待つようだったらjob monitor表示
        # status:doneだったら/なったら、result取ってくる。
        # job_num > self.job_num or job_num < 0 or not( type(job_num) == int )　だったら、raiseする。
        # 最後に、self.flag[job_num-1]["get_result"] = True
        pass  # result[job_num-1][0]=frequencyのlist, result[job_num-1][1]=count（縦軸), result[job_num-1][2] = エラーバーのlist
    
    
    def draw(fitting=False, error=False, Ey=False, E1E2=False, save=False, job_num = 0):
        # optionでfittingするか選べる ← fitingのlistには_make_fittingメソッドを使って下さい。
        # optionでエラーバーいれるか選べる。
        # optionでE1E2,Eyの中心値を表示するか選べる。 ← 中心値にはcalibrationメソッドを使ってください。
        # optionで保存するか選べる。
        # その他、optionを入れる。optionは引数にするが、あくまでoptionなので、選ばなくても良いようにする。
        # runをまだ実行してなかったら(self.mode == None)、エラーを返す。
        pass
    
    
    def laser_draw(fitting=False, Ey=False, E1E2=False, save=False, job_num = 0):
        # optionでfittingするか選べる ← fitingのlistはこちらは簡単だと思うので、自分で作って下さい。
        # optionで保存するか選べる。
        # その他、optionを入れる。optionは引数にするが、あくまでoptionなので、選ばなくても良いようにする。
        # runをまだ実行してなかったら(self.mode == None)、エラーを返す。
        pass

    
    def calibration(self, job_num = 0):  # E1E2とEyのキャリブレーション結果を返す ← E1E2は二つの頂点のちょうど中心を取る。Eyは_make_fittingのself.x0を返す。
        # runをまだ実行してなかったら(self.mode == None)、エラーを返す。
        pass
    
    
    def save(self, job_num = 0):  # jsonにE1とExEy保存する。
        pass
    
        
    def _make_fitting(self, job_num = 0): #Eyについてのfitingのlistを返す（ローレンチアン）、x0とγをself.x0とself.gammaに代入
        # runをまだ実行してなかったら(self.mode == None)、エラーを返す。
        pass
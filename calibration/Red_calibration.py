# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 18:30:33 2022

@author: Yokohama National University, Kosaka Lab
"""

class Red_calibration():
    def __init__(self):
        self.mode = None
    
    def run(self, mode):  # 大輔が作ります
        """
        mode: Ey or E1E2 or all
        どの周りのスペクトルを取るか選べる。
        """
        result = []  # Rabi_project20_E6EL06_area06_NV04_PLE_all_0.txtの内容が入ったlistを返します。
        return result  # result[0]=frequencyのlist, result[1]=count（縦軸), result[2] = エラーバーのlist
    
    def draw(fitting=False, error=False , Ey=False, E1E2=False, save=False):
        # optionでfittingするか選べる ← fitingのlistには_make_fittingメソッドを使って下さい。
        # optionでエラーバーいれるか選べる。
        # optionでE1E2,Eyの中心値を表示するか選べる。 ← 中心値にはcalibrationメソッドを使ってください。
        # optionで保存するか選べる。
        # その他、optionを入れる。optionは引数にするが、あくまでoptionなので、選ばなくても良いようにする。
        # runをまだ実行してなかったら(self.mode == None)、エラーを返す。
        pass
    
    def calibration():  # E1E2とEyのキャリブレーション結果を返す ← E1E2は二つの頂点のちょうど中心を取る。Eyは_make_fittingのself.x0を返す。
        # runをまだ実行してなかったら(self.mode == None)、エラーを返す。
        pass
    
    def _make_fitting(): #Eyについてのfitingのlistを返す（ローレンチアン）、x0とγをself.x0とself.gammaに代入
        # runをまだ実行してなかったら(self.mode == None)、エラーを返す。
        pass
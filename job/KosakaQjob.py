# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 14:19:48 2022

@author: Daisuke Ito
"""
from qiskit.providers.job import JobV1 as Job
from qiskit.providers.jobstatus import JobStatus
from qiskit.result.result import Result
from qiskit.result.models import ExperimentResultData, ExperimentResult
import socket
import os
import json
import time


class KosakaQJob(Job):
    def __init__(
            self,
            backend,
            job_id: str,
            PORT: int,
            _status: str
    ):
        self._backend = backend
        self._job_id = job_id
        self._PORT = PORT
        super().__init__(self.backend(), self.job_id())
    
    def submit(self):
        """Submit the job to the backend for execution."""
        print("This method is not supported\nuse backend.run()")
    
    
    def status(self):
        """Return the status of the job, among the values of ``JobStatus``."""
        
        def receiving(Job_id):
            import sys
            
            PORT = self._PORT
            
            
            class UnsupportedMethod(RuntimeError):
                pass
            
            
            class InvalidData(ValueError):
                pass
            
            
            class ValidationError(ValueError):
                pass
            
            
            class Receive:
                def __init__(self):
                    self.init_recv_worker_sock()
            
                def log(self, msg):
                    print(msg)
            
                def run(self):
                    # サーバーからの接続を受け付ける
                    client_sock, addr = self.recv_worker_sock.accept()
                    
                    # 受信開始
                    try:
                        self.receive(client_sock)
                    except (
                        ConnectionResetError,
                        BrokenPipeError,
                        socket.timeout,
                        UnsupportedMethod,
                        ValidationError,
                        InvalidData,
                    ) as e:
                        print('Error:', e, file=sys.stderr)
                    
                    return self.data
            
                def init_recv_worker_sock(self):
                    # ソケットを作る
                    self.recv_worker_sock = socket.socket(
                        socket.AF_INET,  # IPv4
                        socket.SOCK_STREAM,  # TCP
                    )
                    
                    # ソケットをアドレスとポートに紐づける
                    self.recv_worker_sock.bind(
                        (socket.gethostname(), PORT),
                    )
            
                    # ソケットをパッシブソケット（接続待ちソケット）にする
                    self.recv_worker_sock.listen()
            
                
                def receive(self, sock):
                    # JSONリクエストを受信する
                    try:
                        data = sock.recv(1024)
                    except (
                        ConnectionResetError,
                        BrokenPipeError,
                        socket.timeout,
                    ) as e:
                        raise e
            
                    sdata = data.decode()  # バイト列を文字列に変換
                    d = json.loads(sdata)  # 文字列（JSON）を辞書に変換
            
                    self.receive_json(sock, d)  # 受信処理を続ける
            
                def receive_json(self, sock, d):
                    # methodがPOSTだったら受信を続行する
                    method = d.get('method', '')
                    if method == 'POST':
                        self.receive_post(sock, d)
                    else:
                        raise UnsupportedMethod(f'invalid method "{method}"')
            
                def receive_post(self, sock, d):
                    # ファイル名とファイルサイズを取得
                    fname = d.get('filename', None)
                    fsize = d.get('filesize', None)
                    if fname is None or fsize is None:
                        raise InvalidData('invalid post data')
            
                    # ファイル本体の受信開始
                    bdata = b''
                    while len(bdata) < fsize:
                        try:
                            bdata += sock.recv(1024)
                        except (
                            ConnectionResetError,  # 接続が切れた
                            BrokenPipeError,  # パイプが壊れた
                            socket.timeout,  # タイムアウトになった
                        ) as e:
                            raise e
            
                    self.look_data(fname, bdata)
            
                def look_data(self, fname, bdata):
                    # ファイル名をセキュリティのために検証する
                    self.validate_fname(fname)
                    
                    # 辞書に変換
                    self.data = json.loads(bdata)

                def validate_fname(self, fname):
                    # ファイル名に以下の文字列が含まれていたらエラーにする
                    if '..' in fname or \
                       '/' in fname or \
                       '\\' in fname:
                        raise ValidationError(f'invalid file name "{fname}"')
                
            def sending(job_id):
                PORT = self._PORT
                targetIP = self._backend.IP
                myIP = socket.gethostbyname(socket.gethostname())#userのローカルIP
                fname = str(int(100000*time.time())) + ".json"
                
                json_data = {}
                json_data["userIP"] = myIP
                json_data["job_id"] = job_id
                
                                
                with open(fname, 'w') as fp:
                    json.dump(json_data, fp, indent=4)

                # ファイルを開いて読み込む
                with open(fname, 'rb') as fin:
                    data = fin.read()
                
                os.remove(fname)
                
                # データを1024バイトごとに分割する
                chunks = [data[i:i+1024] for i in range(0, len(data), 1024)]
                
                # ソケットを作って接続する
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((targetIP, PORT))
                # JSONリクエストを送る
                d = json.dumps({
                    'method': 'POST',
                    'filename': fname,
                    'filesize': len(data),
                })
                d = d.encode()  # 文字列をバイト列に変換
                sock.send(d)  # 送信
                #リクエストと間をあける
                time.sleep(1)
                
                # ファイルデータをサーバーに送信する
                for chunk in chunks:
                    sock.send(chunk)
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
    
            send_uncomplete_life = 5
            while send_uncomplete_life>0:
                try:
                    sending(Job_id)
                    send_uncomplete_life = -1
                except:
                    print("Connection failed: Retrying connetion\n")
                    send_uncomplete_life -= 1
                    time.sleep(1)
            #lifeが尽きてwhile脱出してしまったらraise
            if send_uncomplete_life == 0:
                raise Exception('Error: Connection failed')
            data = Receive().run()
            return data
            
        self.data = receiving(self._job_id)
        nowstatus = self.data.get("status")
        if nowstatus == "QUEUED":
            self._status = JobStatus.QUEUED
        elif nowstatus == "VALIDATING":
            self._status = JobStatus.VALIDATING
        elif nowstatus == "RUNNING":
            self._status = JobStatus.RUNNING
        elif nowstatus == "CANCELLED":
            self._status = JobStatus.CANCELLED
        elif nowstatus == "DONE":
            self._status = JobStatus.DONE
        else:
            self._status = JobStatus.ERROR
        
        return self._status

    
    def result(self):
        """Return the results of the job."""        
        
        import random
        self.status()
        while (not (self._status == JobStatus.DONE)):
            time.sleep(random.randrange(8, 12, 1))
            self.status()
            if self._status == JobStatus.CANCELLED or self._status == JobStatus.ERROR:
                raise Exception
        if self.data.get("mode") == "redE1E2" or self.data.get("mode") == "redEy" or self.data.get("mode") == "redall":
            expresult = self.data.get("calib_data")
        else:
            expdata = ExperimentResultData(counts=self.data.get("counts"))
            expresult = ExperimentResult(shots=self.data.get("shots"),success=True,data=expdata)
        final_result = Result(backend_name=self._backend, backend_version="1.0.0", qobj_id=self._job_id ,job_id=self._job_id, success=True, results=[expresult])
        return final_result
        
        
    def queue_position(self):
        # self.status()
        return self.data.get("queue_position")

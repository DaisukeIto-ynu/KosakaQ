# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 13:33:39 2022

@author: Daisuke Ito
"""

class KosakaQ_communicate():
    def __init__(self, qobj, targetIP):
        import socket
        self.targetIP = targetIP
        self.myIP = socket.gethostbyname(socket.gethostname())#userのローカルIP
        self.qobj = qobj
    
    
    def send_jobid_query(self):
        import socket
        import os
        import json
        import time
        PORT = 49999
        fname = str(int(100000*time.time())) + ".json"
        json_data = {}
        json_data["userIP"] = self.myIP

        with open(fname, 'w') as fp:
            json.dump(json_data, fp, indent=4, ensure_ascii=False)
        
        # ファイルを開いて読み込む
        with open(fname, 'rb') as fin:
            data = fin.read()
        
        os.remove(fname)
        
        # データを1024バイトごとに分割する
        chunks = [data[i:i+1024] for i in range(0, len(data), 1024)]
        
        # ソケットを作って接続する
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print((self.targetIP, PORT))
        sock.connect((self.targetIP, PORT))
    
        print('sending job_id_query...')
    
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


    def receive_job_id(self):
        import sys
        import socket
        import json
        
        PORT = 49999
        
        class UnsupportedMethod(RuntimeError):
            pass
        
        
        class InvalidData(ValueError):
            pass
        
        
        class ValidationError(ValueError):
            pass
        
        
        class Serve():
            def __init__(self):
                self.init_recv_worker_sock()
                self.ack = -1
        
            def log(self, msg):
                print(msg)
        
            def run(self):
                # サーバーからの接続を受け付ける
                self.log('Waiting job_id...')
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
                
                return self.job_id
        
            def init_recv_worker_sock(self):
                # ソケットを作る
                self.recv_worker_sock = socket.socket(
                    socket.AF_INET,  # IPv4
                    socket.SOCK_STREAM,  # TCP
                )
                
                # timeout: 10.0s
                self.recv_worker_sock.settimeout(10.0)
                
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
                
                self.job_id = d
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
                self.log(f'connection established.\n job_id: {self.job_id.get("job_id")}\n PORT :{self.job_id.get("PORT")}\n')
        
        return Serve().run()


    def send_file(self,Job_id):
        import socket
        import os
        import json
        import time
        PORT = 50000
        fname = Job_id.get("job_id") + ".json"
        json_data = {}
        json_data["userIP"] = self.myIP
        json_data["filename"] = fname
        json_data["PORT"] = Job_id.get("PORT")
        json_data["qobj"] = self.qobj
        # if "shots" in options:
        #     json_data["shots"] = options["shots"]
        # else:
        #     json_data["shots"] = 1024
                   
        with open(fname, 'w') as fp:
            json.dump(json_data, fp, indent=4, ensure_ascii=False)

        # ファイルを開いて読み込む
        with open(fname, 'rb') as fin:
            data = fin.read()
        
        os.remove(fname)

        # データを1024バイトごとに分割する
        chunks = [data[i:i+1024] for i in range(0, len(data), 1024)]
        
        # ソケットを作って接続する
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.self.targetIP, PORT))
    
        print('sending query...')
    
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
        
        sock.close()



    def receive_msg():
        import sys
        import socket
        import json
        
        PORT = 50000
        
        class UnsupportedMethod(RuntimeError):
            pass
        
        
        class InvalidData(ValueError):
            pass
        
        
        class ValidationError(ValueError):
            pass
        
        
        class Serve():
            def __init__(self):
                self.init_recv_worker_sock()
                self.ack = -1
        
            def log(self, msg):
                print(msg)
        
            def run(self):
                # サーバーからの接続を受け付ける
                self.log('Waiting accept...')
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
                
                return self.ack
        
            def init_recv_worker_sock(self):
                # ソケットを作る
                self.recv_worker_sock = socket.socket(
                    socket.AF_INET,  # IPv4
                    socket.SOCK_STREAM,  # TCP
                )
                
                # timeout: 10.0s
                self.recv_worker_sock.settimeout(10.0)
                
                # ソケットをアドレスとポートに紐づける
                self.recv_worker_sock.bind(
                    (socket.gethostname(), PORT),
                )
        
                # ソケットをパッシブソケット（接続待ちソケット）にする
                self.recv_worker_sock.listen()
        
                self.log('connection established. query sended!\n')
            
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
                                    
                if d.get('mes') == 'ack':
                    self.ack = 0
                else:
                    print(d.get("mes")) 
                
                sock.close()
        
        return Serve().run()
        
        
    
    def receive(PORT):
        import sys
        import socket
        import json
        
        class UnsupportedMethod(RuntimeError):
            pass
        
        
        class InvalidData(ValueError):
            pass
        
        
        class ValidationError(ValueError):
            pass
        
        
        class Serve:
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
        
                self.log('Waiting notifications from Server...')
            
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
                data = json.loads(bdata)
                if data.get("queue") > 0:
                    print(f"Your query is queued at No.{data.get('queue')}\n")
                    self.finish_flag = 0
                else:
                    pass # ここに最終処理を追加 

            def validate_fname(self, fname):
                # ファイル名に以下の文字列が含まれていたらエラーにする
                if '..' in fname or \
                   '/' in fname or \
                   '\\' in fname:
                    raise ValidationError(f'invalid file name "{fname}"')
        
        s = Serve()
        s.run()




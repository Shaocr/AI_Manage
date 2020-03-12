'''
此文件用户用于交互
比如用户和用户之间的对战
还有用户和服务器之间的通信
'''
class User(object):
    def __init__(self,username,uid):
        self.username = username
        self.uid = uid
        self.ip=0
    def connect_server(self):
        pass
    def send_mes(self):
        pass
    def receive_mes(self):
        pass
    def disconnect_server(self):
        pass


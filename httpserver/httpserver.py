from socket import *
import sys
import re
from threading import Thread
from httpsetting import *
import time
import threading

class HttpServer(object):
	"""服务器类，功能主要是从浏览器获取请求，发送到后台，再从后台获取数据返回给浏览器，使用多线程编程来实现并发操作"""
	def __init__(self, addr):
		self.addr = addr
		self.Socket = socket()
		self.Socket.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
	def server_forever(self):
		self.Socket.bind(self.addr)
		self.Socket.listen(5)
		while True:
			cli, cli_addr = self.Socket.accept()
			print(cli_addr,'进行了访问',sep = '')
			t = Thread(target = self.multi,args = (cli,))
			t.daemon = True
			t.start()
	def multi(self, *args):
		cli = args[0]
		info = cli.recv(1024)
		print(info.decode())
		f = open('html/Mypage.html','rb')
		data = f.read()
		# print(data)
		response_head = 'HTTP/1.1 200 OK\r\n'
		response_head += '\r\n'
		response = response_head.encode() + data
		print(response)
		cli.send(response)

if __name__ == '__main__':
	A = HttpServer(ADDR)
	A.server_forever()
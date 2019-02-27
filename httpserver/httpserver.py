#coding = utf-8
'''
name:wangxiong
time:2019-2-26
'''

from socket import *
import sys
import re
from threading import Thread
from setting import *
import time

class HttpServer(object):
	def __init__(self, addr = ('0.0.0.0',80)):
		self.sockfd = socket()
		self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		self.addr = addr
		self.bind(addr)
	def bind(self, addr):
		self.ip = addr[0]
		self.port = addr[1]
		self.sockfd.bind(addr)
	def server_forever(self):
		self.sockfd.listen(5)
		print('监听端口%d中' % self.port)
		while True:
			connfd, addr = self.sockfd.accept()
			print('客户端',addr,'已连接',sep = '')
			#创建多线程
			t = Thread(target = self.handle_request,args = (connfd,))
			t.daemon = True
			t.start()
	def handle_request(self, connfd):
		request = connfd.recv(4096)
		#获取请求行
		request_lines = request.splitlines()
		request_line = request_lines[0].decode()
		#正则提取请求方法和内容
		pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
		try:
			#匹配内容放到字典中，按照捕获组分配
			env = re.match(pattern, request_line).groupdict()
		except:
			resoonse_headlers = 'HTTP/1.1 500 ServerError\r\n'
			resoonse_headlers += '\r\n'
			resoonse_headlers += 'Server Error'
			connfd.send(resoonse_headlers.encode())
			return
		status, response_body = self.send_request(env['METHOD'], end['PATH'])
		#根响应码组织响应头
		response_headlers = self.get_headlers(status)
		#结果组织为http格式发送给客户端
		response = response_headlers + response_body
		connfd.send(response.encode())
		connfd.close()


		#与框架交互，发送request,获取response
	def send_request(self,method,path):
		pass
	def get_headlers(self,status):
		pass
	

if __name__ == '__main__':
	#从配置文件导入了
	httpd = HttpServer(ADDR)       
	httpd.server_forever()
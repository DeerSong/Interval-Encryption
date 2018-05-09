#coding=utf-8
import random
import numpy as np

class Cipher():
	key = []
	data = []
	index = []
	A = []
	l,h = 0,0

	def __init__(self):
		pass

	def loadData(self,data):
		self.data = np.array(data)
		self.l = np.min(data)-1
		self.h = np.max(data)+1

	def genKey(self):
		# 测试矩阵对精度的影响，速度
		M = np.random.randint(-25,25,size=(4,4))
		M_inv = np.linalg.inv(M)
		# 分别删去一行、一列
		M = np.delete(M,2,axis=0)
		M_inv = np.delete(M_inv,3,axis=1)
		# print M
		# print M_inv
		self.key.append(M)
		self.key.append(M_inv)

	def genIndex(self):
		data = self.data
		index = data
		l = self.l
		h = self.h
		#print l,h
		mid = 1.0*(l+h)/2
		diff = 1.0*(h-l)/2
		index = 1.0*(index-mid)/diff # index为cos(θ)
		assert(max(index)<=1+1e-10) # 检测是否会超过界限
		assert(min(index)>=-1-1e-10)
		index = np.array([index])
		A = np.concatenate((index, np.sqrt(1-index*index), np.random.rand(1,index.shape[1])), axis=0)
		A = A.T
		self.A = A
		self.index = np.dot(A,self.key[0])
		# print self.index

	def genTrapDoor(self,L,H):
		M_inv = self.key[1]
		data = self.data
		l = self.l
		h = self.h
		mid = 1.0*(l+h)/2
		diff = 1.0*(h-l)/2

		# print l,h
		# print L,H
		x = 1e-4
		L = 1.0*(L-x-mid)/diff # L,H的cos(θ)
		H = 1.0*(H+x-mid)/diff
		L_sin = np.sqrt(1-L*L)
		H_sin = np.sqrt(1-H*H)
		# print L_sin,H_sin
		T_L = np.dot(M_inv,np.transpose([L,L_sin,np.random.rand(1,1)])) # 这里的随机数?
		T_H = np.dot(M_inv,np.transpose([H,H_sin,np.random.rand(1,1)]))
		T_range = L*H + L_sin*H_sin
		return np.array([T_L,T_H,T_range])

	def getKey(self):
		return self.key[1] # 返回私钥M_inv

	def getIndex(self):
		return self.index

	def genTestIndex(self):
		data = self.data[:4]
		# print data
		l,h = self.l,self.h
		mid = 1.0*(l+h)/2
		diff = 1.0*(h-l)/2
		data = 1.0*(data-mid)/diff
		# print data
		data = np.arccos(data)
		# print data
		index = self.index[:4]
		# print index
		print (data,index)
		return (data, index)
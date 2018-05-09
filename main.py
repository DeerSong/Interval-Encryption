#coding=utf-8
import numpy as np
import random
from cipher import Cipher
from decipher import Decipher

def test(N,M):
	l,h = -1000,1000
	data = [random.randint(l,h) for i in range(N)]
	C = Cipher()
	C.genKey() # 生成私钥M,M_inv
	C.loadData(data) # 加载数据
	C.genIndex() # 由数据生成索引index
	C.genTestIndex()

	D = Decipher()
	D.loadKey(C.getKey()) # 服务器获取M_inv私钥
	D.loadIndex(C.getIndex()) # 服务器获取index
	# M次查询对拍测试
	for j in range(M):
		# 随机生成查询区间
		# ll = random.randint(min(data),max(data))
		# hh = random.randint(min(data),max(data))
		# if hh < ll:
		# 	ll,hh = hh,ll
		# ll = random.randint(min(data),max(data)) # 此时会把最小值包含进去
		hh = min(data)
		ll = min(data) # 包含最小值
		# hh = random.randint(min(data),max(data))
		# ll = data[0]
		# hh = data[0]
		Trap = C.genTrapDoor(ll,hh) # 生成陷门
		ans = D.searchData(Trap) # 解密的结果
		ans2 = [i for i in range(N) 
			if ll<=data[i] and data[i]<=hh] # 正确答案
		print ans
		print ans2
		print ll,hh
		if set(ans)!=set(ans2):	
			print "ERROR!!"
			for k in range(N):
				if data[k] == hh:
					break
			print "Trap!!!"
			print Trap[0]
			print Trap[1]
			print C.A[k]
			print C.index[k]
			print data
			print "XXXXXXXXXXXXXXX!!!!"
			print j
			return -1
	print "Success!!"

def hack(N):
	def indexMinus(i,j):
		return (cos[i]*index[j]-cos[j]*index[i])

	def sinMinus(i,j):
		return sin[i]*cos[j] - cos[i]*sin[j]

	l,h = -1000,1000
	data = [random.randint(l,h) for i in range(N)]
	# print(min(data),max(data))
	C = Cipher()
	C.genKey() # 生成私钥M,M_inv
	C.loadData(data) # 加载数据
	C.genIndex() # 由数据生成索引index

	data, theta, index = C.genTestIndex()
	# print(data)
	# print(theta)
	# print(index)
	cos,sin = theta[0],theta[1]
	u3 = indexMinus(1,0)*sinMinus(1,2)-indexMinus(2,1)*sinMinus(0,1)
	print("u3=")
	print(u3)
	print("M4=")
	print(C.key[0][2])
	print(C.key[0])
	u3.shape = [4,1]
	# u3 = np.transpose(u3)
	# print(u3)

	tmp = []
	for i in range(3):
		a = np.eye(4)*cos[i]
		b = np.eye(4)*sin[i]
		c = np.zeros([4,3])
		for j in range(4):
			c[j][i] = u3[j]
		# print(c)
		d = np.concatenate((a,b,c),axis=1)
		# for j in d:
		# 	print j
		tmp.append(d)
	A = np.concatenate(tmp,axis=0)
	# print A.shape
	# print A

	b = index[:3]
	# print(b)
	b.shape=[12,]
	# 求解u1,u2,k1,k3,k3共11个未知数的超定方程组
	X = np.linalg.solve(np.dot(A.T.copy(),A),np.dot(A.T.copy(),b))
	print("X=")
	print(X[0:4])
	print(X[4:8])
	print(X[8:11])

	u1 = X[0:4]
	u2 = X[4:8]
	k = X[8:11]
	for i in range(3):
		i1 = cos[i]*u1+sin[i]*u2+k[i]*u3.transpose()
		print(i1)
		print(index[i])

if __name__ == '__main__':
	# test(100,1)
	hack(100)
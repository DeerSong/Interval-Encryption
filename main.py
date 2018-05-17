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

	def isCorrelated(x,y,s):
		print(s)
		x.shape = [1,x.shape[0]]
		y.shape = [y.shape[0],1]
		cos = np.dot(x,y)/np.linalg.norm(x)/np.linalg.norm(y) # cos值
		if abs(cos)>0.999:
			return True
		return False

	def solve(n):
		tmp = []
		for i in range(n):
			a = np.eye(4)*cos[i]
			b = np.eye(4)*sin[i]
			c = np.zeros([4,n])
			for j in range(4):
				c[j][i] = u4[j]
			d = np.concatenate((a,b,c),axis=1)
			tmp.append(d)
		A = np.concatenate(tmp,axis=0)
		print(A.shape)
		# print A
		# A = A[:-1][:]
		# print A

		b = index[:n]
		b.shape=[n*4,]
		# print(b)
		# b = b[:-1]
		# print(b)

		A,b = np.dot(A.T,A),np.dot(A.T,b)
		# 以下3行是用来测试行列式计算求解方程的正确性的：修改A,b,方程矩阵的大小
		# A = np.array([[2,3,-5],[1,-2,1],[3,1,3]]) 
		# b = np.array([3,0,7])
		# l = 3
		l = 8+n
		D = np.linalg.det(A)
		X = np.zeros([l])
		print(A.shape)
		for i in range(l):
			Ai = np.array(A)
			for j in range(l):
				Ai[j][i] = b[j]
			Di = np.linalg.det(Ai)
			X[i] = Di/D
		# print(u"X= 行列式方法")
		# print(X)
		# print(np.dot(A,X)-b)
		# return X
		
		# 求解u1,u2,k1,k2,k3共11个未知数的超定方程组
		X = np.linalg.solve(A,b)
		# print(u"X= numpy自带方法")
		# print(X)
		# print(np.dot(A,X)-b)
		return X

	l,h = -1000,1000
	data = [random.randint(l,h) for i in range(N)]
	# print(min(data),max(data))
	C = Cipher()
	C.genKey() # 生成私钥M,M_inv
	C.loadData(data) # 加载数据
	C.genIndex() # 由数据生成索引index

	data, theta, index = C.genTestIndex()
	cos,sin = theta[0],theta[1]
	u4 = indexMinus(1,0)*sinMinus(1,2)-indexMinus(2,1)*sinMinus(0,1)
	# print("u4=")
	# print(u4)
	# print("M4=")
	# print(C.key[0][2]) # 私钥M的最后一行，u4
	print(isCorrelated(u4,C.key[0][2],u"u4'与u4是否线性相关"))
	print("")
	print("M=")
	print(C.key[0]) # 私钥M
	u4.shape = [4,1]

	X = solve(3) # 求解u1,u2,k1,k2,k3
	u1,u2,k = X[0:4],X[4:8],X[8:11]

	print("X=")
	print(u1)
	print(u2)
	print(k)

	print("")
	print(isCorrelated(u1-C.key[0][0],u4,u"u1'-u1与u4是否线性相关"))
	print(isCorrelated(u2-C.key[0][1],u4,u"u2'-u2与u4是否线性相关"))

	print("")
	print(u"验证M’*N是否为[[1,0,0],[0,1,0],[0,0,0]]")
	print(u"伪造索引值成功！")
	u1.shape,u2.shape,u4.shape = [1,4],[1,4],[1,4]
	M1 = np.concatenate((u1,u2,u4),axis=0)
	print(np.dot(M1,C.key[1]))

	# u4 = 2*u4 # 检查u4乘以一个实数之后，解是否满足u1,u2不变
	# # u4 = C.key[0][2] # 检查把u4直接赋值为真实私钥，解是否满足u1,u2不变
	# # u4.shape = [4,1]
	# # print(u4)
	# X = solve(3)
	# u1,u2,k = X[0:4],X[4:8],X[8:11]

	# print("X=")
	# print(u1)
	# print(u2)
	# print(k)

	print("")
	print(u"检验真实index与生成index是否相等")
	u4.shape = [4,1]
	# 检查由X生成的index是否与真实的相等，现在是相等的
	for i in range(3):
		i1 = cos[i]*u1+sin[i]*u2+k[i]*u4.transpose()
		print(i1)
		print(index[i])

if __name__ == '__main__':
	# test(100,1)
	hack(100)
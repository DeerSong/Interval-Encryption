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

	def solve(n):
		tmp = []
		for i in range(n):
			a = np.eye(4)*cos[i]
			b = np.eye(4)*sin[i]
			c = np.zeros([4,n])
			for j in range(4):
				c[j][i] = u3[j]
			# print(c)
			d = np.concatenate((a,b,c),axis=1)
			# for j in d:
			# 	print j
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
		# 求解u1,u2,k1,k2,k3共11个未知数的超定方程组
		X = np.linalg.solve(np.dot(A.T,A),np.dot(A.T,b))
		return X

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
	# 可以发现是线性相关的
	print("u3=")
	print(u3)
	print("M4=")
	print(C.key[0][2]) # 私钥M的最后一行，u4
	print(C.key[0]) # 私钥M
	u3.shape = [4,1]

	X = solve(50) # 求解u1,u2,k1,k2,k3
	u1 = X[0:4]
	u2 = X[4:8]
	k = X[8:11]

	print("X=")
	print(u1)
	print(u2)
	print(k)

	u3 = 2*u3 # 检查u4乘以一个实数之后，解是否满足u1,u2不变
	# u3 = C.key[0][2] # 检查把u4直接赋值为真实私钥，解是否满足u1,u2不变
	# u3.shape = [4,1]
	# print(u3)
	X = solve(3)
	u1 = X[0:4]
	u2 = X[4:8]
	k = X[8:11]

	print("X=")
	print(u1)
	print(u2)
	print(k)

	print("")
	# 检查由X生成的index是否与真实的相等，现在是相等的
	for i in range(3):
		i1 = cos[i]*u1+sin[i]*u2+k[i]*u3.transpose()
		print(i1)
		print(index[i])

if __name__ == '__main__':
	# test(100,1)
	hack(100)
import numpy as np
class Decipher():
	key_inv = []
	index = []
	def __init__(self):
		pass
	def loadKey(self,key):
		# print key
		self.key_inv = key
	def loadIndex(self,index):
		# print index
		self.index = index
	def searchData(self,Trap):
		ans = []
		k = 0
		index = self.index
		for i in index:
			t = np.dot(i,np.transpose(Trap[0])) * np.dot(i,np.transpose(Trap[1]))
			if Trap[2] < t:
				ans.append(k)
			k += 1
		return ans
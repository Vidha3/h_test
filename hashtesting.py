__author__ = 'Vidhathri Kota'
__author__ = 'Mary Shilpa Thumma'
from collections import namedtuple
import re
import sys
Entry = namedtuple('Entry', ('key', 'value'))
class Hashing:
	__slots__ = "table", "num", "cap", "maxload", "hashtype", "probe", "collision"
	def __init__(self, hashtype=0, in_cap=100, maxload=0.7):
		'''
           Creates an open-addressed hash map of given size and maximum load factor
                :param initsz: Initial size in_cap (default 100)
                :param hashtype: there are 2 functions so the type of hash is determined by the parameter
                :param maxload: Max load (factor) (default 0.7)
		'''

		self.num = 0
		self.hashtype = hashtype
		self.cap = in_cap
		self.table = [None for _ in range(self.cap)]
		self.probe = 0
		self.collision = 0
		self.maxload = maxload

	def hash_one(self, key):
		'''
		Calculates a hash value based on the position of each character, ASCII value and the previous hash value
			:param: key for which hash is calculated
			:return: the hash value
		'''
		sum = 1

		for i in range(len(key)):
			sum = sum * ord(key[i])//(i+1)
		return sum

	def hash_two(self, key):
		'''
		Calculates a hash value based on the position, ASCII value and the previous hash value; uses left shift
			:param: key for which hash is calculated
			:return: the hash value
		'''
		digits=len(key)
		div=key
		div.split()
		sum = 0
		for i in range (digits):
			sum=sum+((ord(div[i])))<<i
		#hash= sum % digits
		return sum

	def put(self, word, value):
		'''
                Adds the given (key,value) to the map, replacing entry with same key if present.
                :param word: Key or word of new entry
                :param value: Value of new entry of the number of times it has appeared
                if for the same key or the same word if the hash value generated is same
                then a collision occurs
                It is handled by placing the word in the next immediate index
                The number of times the control has searched for an index for the presence of
                the key or the word, then the probe count increases.
		'''
		if self.hashtype == 1:
			hashval = self.hash_one(word)
		elif self.hashtype == 2:
			hashval = self.hash_two(word)
		else:
			hashval = hash(word)   #built in hash
		index = hashval % self.cap
		if self.table[index] != None:
			self.collision += 1
		while self.table[index] != None and self.table[index].key != word:
				index += 1
				self.probe += 1
				if index == len(self.table):
					index = 0
		if self.table[index] is None:
			self.num += 1
		self.table[index] = Entry(word,value)
		if self.num/self.cap > self.maxload:
		# rehashing
			oldtable = self.table
			# refresh the table
			self.cap *= 2
			self.table = [None for _ in range(self.cap)]
			self.num = 0
			# put items in new table
			for entry in oldtable:
				if entry is not None:
					self.put(entry[0],entry[1])

	def get(self,key):
		'''
		Return the value associated with the given key
                :param key: Key to look up
                :return: Value (or KeyError if key not present)
		'''

		if self.hashtype == 1:
			hashval = self.hash_one(key)
		elif self.hashtype == 2:
			hashval = self.hash_two(key)
		else:
			hashval = hash(key)   #built in hash
		index = hashval % self.cap
		while self.table[index] is not None and self.table[index].key != key:
			index += 1
			self.probe += 1
			if index == self.cap:
				index = 0
		if self.table[index] is not None:
			return self.table[index].value
		else:
			raise KeyError('Key ' + str(key) + ' not present')

	def contains(self, word):
		'''
		 Returns True/False whether key is present in map
               :param key: Key to look up
               :return: Whether key is present (boolean)
		'''
		if self.hashtype == 1:
			hashval = self.hash_one(word)
		elif self.hashtype == 2:
			hashval = self.hash_two(word)
		else:
			hashval = hash(word)   #built in hash
		index = hashval % self.cap
		while self.table[index] is not None and self.table[index].key != word:
			index += 1
			self.probe += 1
			if index == self.cap:
				index = 0
		return self.table[index] is not None

def count(obj,word):
	'''
	Takes a word and adds it to the hash map
           :param word: word to be added
           :param obj: the object of hashmap class to which the word is added
	'''
	if obj.contains(word):
		c = obj.get(word)
		obj.put(word, c + 1)
	else:
		obj.put(word, 1)

def max(obj):
	'''
	Returns the key, value pair such that key is the word with maximum value
	That is, has appeare max no. of times
		:param obj - the hashing object for which max is to be calculated
		:Return (key,m)- the key and corresponding value
	'''
	index = 0
	m = 0
	key = ''
	for index in range(obj.cap):
		if obj.table[index] != None:
			if obj.table[index].value > m:
				m = obj.table[index].value
				key = obj.table[index].key
			#print(obj.table[index].key," ",obj.table[index].value)
	return (key, m)

def printMap(map):
    for i in range(map.cap):
        print(str(i)+": " + str(map.table[i]))

def main():
	f = open(sys.argv[1],"r",encoding="UTF-8")
	text = f.read()
	words = re.split('\W+',text)
	one=list()
	two=list()
	three=list()
	for i in range(3):
		one.append(Hashing(1, 200, 0.5+(0.2*i)))	#tests hash_one
		two.append(Hashing(2, 200, 0.5+(0.2*i)))	#tests hash_two
		three.append(Hashing(0, 200, 0.5+(0.2*i)))	#tests built in hash
	for i in range(3):
		for j in words:
			j.lower()
			count(one[i], j)
			count(two[i], j)
			count(three[i], j)
	print("Maxload    Collision")
	print("\thash_one  hash_two   built-in")
	for i in range(3):
		print(one[i].maxload,"\t",one[i].collision," ",two[i].collision," ",three[i].collision)
	print("\nMaxload     Probe")
	print("\thash_one  hash_two   built-in")
	for i in range(3):
		print(one[i].maxload,"\t",one[i].probe," ",two[i].probe," ",three[i].probe)
	print("Files added to both dictionaries.")
	(most, freq) = max(one[1])
	print("Function #1: The word of highest frequency:", most,". Frequency: ",freq)

if __name__=="__main__":
	main()		



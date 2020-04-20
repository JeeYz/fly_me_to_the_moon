# Making a class in python.
# This file is just practice. 

print("hello, world~!")

class A:
	def __init__(self):
		print("Class A __init__()")
		super(A, self).__init__()

class B(A):
	def __init__(self):
		print("Class B __init__()")
		print("__B")
		#A.__init__(self)
		super(B, self).__init__()

class C(A):
	def __init__(self):
		print("Class C __init__()")
		print("__C")
		#A.__init__(self)
		super(C, self).__init__()

class D(B, C):
	def __init__(self):
		print("Class D __init__()")
#		B.__init__(self)
#		C.__init__(self)
		super(D, self).__init__()

d = D()



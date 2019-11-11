# @Author: J.Y.
# @Date:   2019-11-07T23:35:30+09:00
# @Last modified by:   J.Y.
# @Last modified time: 2019-11-12T03:24:40+09:00
# @License: J.Y. JeeYz
# @Copyright: J.Y. JeeYz

import numpy as np

print('hello, world~!')

a = list()
b = [1, 2]

print(a)

a.insert(0, b)

print(a)

c = np.zeros((10, 10))
print(c)
print(type(c))

c = c.tolist()

print(c)
print(type(c))


class stack():
    def __init__(self):
        self.stack_cell = list()

d = stack()
d.stack_cell.insert(0, 'wwyd')
c[0][0] = d

print(c)

for i in c:
    print(i)

print('\n\n')

print(c[0][0].stack_cell[0])


print('\n\n')

# c[4].insert(5, 'john')
c[4][5] = 'john'
for i in c:
    print(i)


print('\n\n')


a = list()
a.append('john')
print(a)
a.append('james')
print(a)
del a[0]
print(a)


print('\n\n')

a = np.zeros((10, 10))
print(a)
print(len(a))











## endl

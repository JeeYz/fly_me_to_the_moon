# @Author: J.Y.
# @Date:   2019-10-21T07:31:58+09:00
# @Last modified by:   J.Y.
# @Last modified time: 2019-11-07T23:34:11+09:00
# @License: J.Y. JeeYz
# @Copyright: J.Y. JeeYz

import numpy as np

a = np.random.rand(2, 3)

print(a)
print(type(a))

print('\n\n')

a = a.tolist()

print(a)
print(type(a))

print('\n\n')

b = np.zeros((3, 4))

print(b)

print('\n\n')

c = np.random.rand(10)
print(c)
print(type(c))
print(len(c))


## endl

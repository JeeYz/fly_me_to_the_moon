for i in range(2,5+1):
    print(i)


a = [[1, 2], [2, 1], [1, 3], [3, 1]]
print(a[:-2])
print(type(a))
# b = set(a)
b = set(a[0])
print(type(b))


c = {1:[4,6], 6:4, 0:[7,0], 8:4, 7:2, 3:[3,7]}

print(c)
print(type(c))
# d = sorted(c.keys())
# print(d)
#
# for i in d:
#     print(c[i])
#

c = dict(sorted(c.items()))
print(c)

for i in c:
    print(c[i])

# e = '"id": 0,'
e = '{"id": 0, "text": "올림픽", "type": "", "begin": 0, "end": 0}'
f = e.split('"')
print(f)

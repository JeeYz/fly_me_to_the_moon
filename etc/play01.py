# @Author: J.Y.
# @Date:   2019-10-21T01:55:00+09:00
# @Last modified by:   J.Y.
# @Last modified time: 2019-12-10T15:45:26+09:00
# @License: J.Y. JeeYz
# @Copyright: J.Y. JeeYz


import numpy as np
import time
import copy

class node():
    def __init__(self):
        self.score = 0
        self.child_left = list()
        self.child_right = list()
        self.end = 'not end'

class cyk_table():
    def __init__(self, r_table):
        temp = len(r_table)
        self.length = temp
        self.input_table = r_table
        temp_matrix = np.zeros((temp+1, temp+1))
        self.matrix = temp_matrix.tolist()
        self.result = self.main()

    def main(self):

        # initiate the first line
        for e in range(1, self.length+1):
            temp = node()
            temp.end = 'end'
            self.matrix[1][e] = temp

        # cyk algorithm
        for lg in range(2, self.length+1):
            for e in reversed(range(lg, self.length+1)):
                temp_stack = list()
                for k in range(1, lg):
                    temp = node()
                    temp.score = self.calculate_cell(lg, e, k)
                    temp.child_left = [k, e-lg+k]
                    temp.child_right = [lg-k, e]
                    temp_stack.append(temp)

                max_node = self.choose_max(temp_stack)
                self.matrix[lg][e] = temp_stack[max_node]

        result = self.retrieve_tree()
        result.sort()
        return result

    def calculate_cell(self, lg, e, k):
        return_value = 0.0
        a = self.matrix[k][e-lg+k]
        b = self.matrix[lg-k][e]
        c = self.input_table[e-lg+k-1][e-1]
        return a.score + b.score + c

    def choose_max(self, stacklist):
        max = 0.0
        max_node = 0
        for i, j in enumerate(stacklist):
            if i == 0.0:
                max = j.score
                max_node = i
            elif j.score > max:
                max = j.score
                max_node = i

        return max_node

    def retrieve_tree(self):
        a = self.matrix[self.length][self.length]
        b = a.child_left # list
        c = a.child_right # list
        stack_list = list()
        result = list()

        stack_list.append(b)
        stack_list.append(c)
        result.append([b[1], c[1]]) # Check it later

        while True:
            if stack_list == []:
                break
            d = stack_list[0] # = list
            e = self.matrix[d[0]][d[1]]
            if e.end == 'end':
                del stack_list[0]
            else:
                b = e.child_left # list
                c = e.child_right # list
                stack_list.append(b)
                stack_list.append(c)
                result.append([b[1], c[1]]) # Check it later
                del stack_list[0]

        return result




if __name__ == '__main__':
    print('hello, world~!')
    print('\n\n\n')

    a = 20
    t_0 = np.random.rand(a, a)
    t_0 = t_0.tolist()
    cyk_0 = cyk_table(t_0)
    cyk_0.result.append([len(t_0), 0])
    for j in cyk_0.result:
        print(j)







## endl

# coding=utf-8
"""ASCII matrix from values. Order of values: left-right bottom-top"""

class Matrix(object):

    def __init__(self, values, num_x, num_y):

        self.values = values
        self.num_x = num_x
        self.num_y = num_y
        self.ASCII_matrix = self.__create_ASCII_matrix()
    

    def __create_ASCII_matrix(self):

        if (len(self.values) != self.num_x * self.num_y):
            raise Exception("Length of values have to be {0}.".format(self.num_x * self.num_y))

        nested_grid = []
        for i in range(0, len(self.values), self.num_x):
            chunck = self.values[i : i + self.num_x]
            nested_grid.append(chunck)
        
        matrix = []
        for j in range(self.num_y-1, -1, -1):
            line = []
            for i in range(self.num_x):
                line.append(str(nested_grid[j][i]))
            text = ' '.join(line)
            matrix.append(text)
            
        return '\n'.join(matrix)
    

    def ToString(self):
        return 'ShrimpGIS::ASCII::{}'.format(len(self.values))
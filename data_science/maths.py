import math
import random

class Vect:
    '''Create a vector'''
    def __init__(self, *args):
        self.args = args
        self.dim = len(self)

    def scalar_product(self, v):
        if not isinstance(v, Vect):
            raise TypeError(f'Execpt a Vect object, got a {v.__class__.__name__} instead')
        self.check_len(v)

        return sum([i * j for i, j in zip(self.args, v.args)])

    def norm(self):
        return math.sqrt(sum([x**2 for x in self.args]))

    def check_instance(self, v):
        if not isinstance(v, Vect) and not isinstance(v, float) and not isinstance(v, int):
            raise TypeError(f'Execpt a Vect, int or float object, got a {v.__class__.__name__} instead')

    def check_len(self, v):
        if len(v) != len(self):
            raise Exception(f'Vector must be same lenght. ({len(self)}) ({len(v)})')

    def __add__(self, v):
        self.check_instance(v)

        if isinstance(v, Vect):
            self.check_len(v)
            args = [i + j for i, j in zip(self.args, v.args)]
        else:
            args = [i + v for i in self.args]

        return self.__class__(*args)

    def __sub__(self, v):
        self.check_instance(v)

        if isinstance(v, Vect):
            self.check_len(v)
            args = [i - j for i, j in zip(self.args, v.args)]
        else:
            args = [i - v for i in self.args]

        return self.__class__(*args)

    def __mul__(self, v):
        self.check_instance(v)

        if isinstance(v, Vect):
            self.check_len(v)
            args = [i * j for i, j in zip(self.args, v.args)]
        else:
            args = [i * v for i in self.args]

        return self.__class__(*args)

    def __len__(self):
        return len(self.args)

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError('Index must be int')

        if item > len(self) - 1 or item < -len(self):
            raise IndexError('Index out of range')

        return self.args[item]

    def __setitem__(self, key, value):
        if not isinstance(key, int):
            raise TypeError('Index must be int')

        self.args = list(self.args)
        self.args[key] = value
        self.args = tuple(self.args)

        if key > len(self) - 1 or key < -len(self):
            raise IndexError('Index out of range')


    def __repr__(self):
        args = ', '.join([str(x) for x in self.args])
        return f"{self.__class__.__name__}({args})"

    @staticmethod
    def angle(u, v):

        if len(u) != len(v):
            raise Exception(f'Vector must be same lenght. ({len(u)}) ({len(v)})')

        if not isinstance(u, Vect):
            raise TypeError(f'{u.__name__} must be Vect')

        if not isinstance(v, Vect):
            raise TypeError(f'{v.__name__} must be Vect')

        return math.acos((u.scalar_product(v)/(u.norm()*v.norm())))

    @classmethod
    def random_unit(cls, n):
        random_values = [random.gauss(0, 1) for _ in range(n)]

        vect = cls(*random_values)

        return vect*(1/vect.norm())

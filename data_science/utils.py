from time import time
import pickle
from typing import Any

class ContextTimer:
    '''Used as a context manager for timing execution of code'''
    number_of_timers = 0

    def __init__(self, title, decimal=2):
        self.title = title
        self.decimal = decimal
        self.label = self.get_number_of_timers()
        self.add_timer()

    def __enter__(self):
        print(f'\n({self.label}) ' + self.title + ':')
        self.start = time()

        return self.title

    def __exit__(self, type_, value, traceback):
        self.end = time()
        t = round(self.end - self.start, self.decimal)

        if type_ is not None: success = 'Error'
        else: success = 'Done'

        print(f'({self.label}) {success} {t} s\n')
        #self.remove_timer()

    @classmethod
    def add_timer(cls):
        cls.number_of_timers += 1

    @classmethod
    def remove_timer(cls):
        cls.number_of_timers -= 1

    @classmethod
    def clear_timers(cls):
        cls.number_of_timers = 0

    @classmethod
    def get_number_of_timers(cls):
        return cls.number_of_timers    


def timer(function_to_time):
    '''Used as a decorator for timing a function'''
    def timed_function(*args, **kwargs):

        start = time() # Get start time
        result = function_to_time(*args, **kwargs) # Execute the fonction and store the result
        t = time() - start # Get end time and substract with start time

        print(f'Function {function_to_time.__name__} took {round(t, 2)} second(s) to be executed.') # Print execution time

        return result # Return the result

    return timed_function # Return the timed function


def join_paths(*paths):
    full_path = paths[0]
    for p in paths[1:]:
        if full_path[-1] == ':':
            full_path += '\\'
        full_path = os.path.join(full_path, p)

    return full_path


number_type = [int, float]

class MyRangeIterator:

    def __init__(self, start: number_type, end: number_type, step: number_type = 1):
        self.current = start
        self.start = start
        self.end = end
        self.step = step
        
    def check_stop_iteration(self) -> None:
        if self.step >= 0:
            if self.current >= self.end:
                raise StopIteration
        else:
            if self.current <= self.end:
                raise StopIteration
            
    def __iter__(self):
        return self
    
    def __next__(self):
        
        self.check_stop_iteration()
            
        val = self.current
        
        self.current += self.step
        
        return val


class MyRange:
    
    def __init__(self, start: number_type, end: number_type, step: number_type = 1):
        self.start = start
        self.end = end
        self.step = step
        
    def __iter__(self):
        return MyRangeIterator(start=self.start, end=self.end, step=self.step)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.start}, {self.end}, {self.step})"


def save_model(model, filepath: str = 'model.pkl') -> None:
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)

def load_model(filepath: str) -> Any:
    with open(filepath, 'rb') as f:
        model = pickle.load(f)

    return model

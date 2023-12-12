'''
RASP OPERATORS THAT ARE SUPPORTED BY TRACR'S PYTHON EMBEDDING
This file contains Python classes that define the rasp operators supported by TRACR's python embedding of the langauge.
This is subset of everything that TRACR supports in python, due to project time constraints.
'''
import random
from typing import (Any, Callable, Dict, Generic, List, Mapping, Optional,
                    Sequence, TypeVar, Union)
from tracr.rasp import rasp
import subprocess
import time

'''
CLASS DEFINITIONS
'''
class Tokens:
    '''
    Tokens constant.
    '''
    def __init__(self):
        self.n_args = 0
        self.arg_types = []
        self.return_type = rasp.SOp
        self.weight = 1
    
    def to_python(self):
        # return an object that can be compiled into a TRACR transformer
        # arguments should be python objects
        return rasp.tokens
    
    def str(self):
        # represent rasp operator in string form
        # expects arguments to be strings
        return "tokens"
    
class Indices:
    def __init__(self):
        self.n_args = 0
        self.arg_types = []
        self.return_type = rasp.SOp
        self.weight = 1
    
    def to_python(self):
        # return an object that can be compiled into a TRACR transformer
        # arguments should be python objects
        return rasp.indices
    
    def str(self):
        # represent rasp operator in string form
        # expects arguments to be strings
        return "indices"

class Zero:
    def __init__(self):
        self.n_args = 0
        self.arg_types = []
        self.return_type = int
        self.weight = 1
    
    def to_python(self):
        # return an object that can be compiled into a TRACR transformer
        # arguments should be python objects
        return 0
    
    def str(self):
        # represent rasp operator in string form
        # expects arguments to be strings
        return "0"

class One:
    def __init__(self):
        self.n_args = 0
        self.arg_types = []
        self.return_type = int
        self.weight = 1
    
    def to_python(self):
        # return an object that can be compiled into a TRACR transformer
        # arguments should be python objects
        return 1
    
    def str(self):
        # represent rasp operator in string form
        # expects arguments to be strings
        return "1"

class Equal:
    '''
    Comparison Equal constant.
    '''
    def __init__(self):
        self.n_args = 0
        self.arg_types = []
        self.return_type = rasp.Predicate
        self.weight = 1
    
    def to_python(self):
        # return an object that can be compiled into a TRACR transformer
        # arguments should be python objects
        return rasp.Comparison.EQ
    
    def str(self):
        # represent rasp operator in string form
        # expects arguments to be strings
        return "=="

class GT:
    '''
    Greater Than comparison operator.
    '''
    pass

class LT:
    '''
    Less Than comparison operator
    '''
    pass

class LEQ:
    pass

class GEQ:
    pass

class TRUE:
    '''
    Comparison True constant.
    '''
    def __init__(self):
        self.n_args = 0
        self.arg_types = []
        self.return_type = rasp.Predicate
        self.weight = 1
    
    def to_python(self):
        # return an object that can be compiled into a TRACR transformer
        # arguments should be python objects
        return rasp.Comparison.TRUE
    
    def str(self):
        # represent rasp operator in string form
        # expects arguments to be strings
        return "true"

class FALSE:
    pass

class Add:
    '''
    Element-wise.
    Input can be either int, float or s-op.
    '''
    pass

class Subtract:
    '''
    Element-wise.
    Input can be either int, float or s-op.
    '''
    def __init__(self):
        self.n_args = 2
        self.arg_types = [Union[rasp.SOp, float, int], Union[rasp.SOp, float, int]]
        self.return_type = Union[rasp.SOp, int, float]
        self.weight = 1
    
    def to_python(self, x, y):
        # return an object that can be compiled into a TRACR transformer
        # arguments should be python objects
        if type(x) == type(rasp.tokens):
            return None
        if type(y) == type(rasp.tokens):
            return None
        return x - y
    
    def str(self, x, y):
        # represent rasp operator in string form
        # expects arguments to be strings
        return f"{x} - {y}"

class Mult:
    '''
    Element-wise.
    Input can be either int, float or s-op.
    '''
    pass

class Divide:
    '''
    Element-wise.
    Input can be either int, float or s-op.
    '''
    pass

class Fill:
    '''
    Given fill value and length, returns Sop of that length with that fill value.
    Fill value can be int, float, or char.
    Length must be a positive integer.
    '''
    pass

class SelectorAnd:
    '''
    Input can be bool or s-op.
    '''
    pass

class SelectorOr:
    '''
    Input can be bool or s-op.
    '''
    pass

class SelectorNot:
    '''
    Input is an s-op of bools. (Or bool-convertible values.)
    '''
    pass

class Select:
    '''
    Select operator.
    '''
    def __init__(self):
        self.n_args = 3
        self.arg_types = [rasp.SOp, rasp.SOp, rasp.Predicate]
        self.return_type = rasp.Selector 
        self.weight = 1
    
    def to_python(self, sop1, sop2, comp):
        # return an object that can be compiled into a TRACR transformer
        # arguments should be python objects
        return rasp.Select(sop1, sop2, comp)
    
    def str(self, sop1, sop2, comp):
        # represent rasp operator in string form
        # expects arguments to be strings
        return f"select({sop1}, {sop2}, {comp})"

class Aggregate:
    '''
    The Aggregate operator.
    '''
    def __init__(self):
        self.n_args = 2
        self.arg_types = [rasp.Selector, rasp.SOp]
        self.return_type = rasp.SOp
        self.weight = 1
    
    def to_python(self, sel, sop):
        # return an object that can be compiled into a TRACR transformer
        # arguments should be python objects
        return rasp.Aggregate(sel, sop)
    
    def str(self, sel, sop):
        # represent rasp operator in string form
        # expects arguments to be strings
        return f"aggregate({sel}, {sop})"

class SelectorWidth:
    '''
    The selector_width operator.
    '''
    def __init__(self):
        self.n_args = 1
        self.arg_types = [rasp.Selector]
        self.return_type = rasp.SOp 
        self.weight = 1
    
    def to_python(self, sel):
        # return an object that can be compiled into a TRACR transformer
        # arguments should be python objects
        return rasp.SelectorWidth(sel)
    
    def str(self, sel):
        # represent rasp operator in string form
        # expects arguments to be strings
        return f"select_width({sel})"

'''
GLOBAL CONSTANTS
'''

# define operators
rasp_operators = [Select(), SelectorWidth(), Aggregate(), Subtract()]
rasp_consts = [Tokens(), Tokens(), Equal(), TRUE(), Indices(), Indices(), Zero(), One()]
'''
TESTING
'''
if __name__ == "__main__":
    test_select = Select()
    
    test_select_python = test_select.to_python(Tokens().to_python(), Tokens().to_python(), Equal().to_python())
    actual_ts_python = rasp.Select(rasp.tokens, rasp.tokens, rasp.Comparison.EQ)
    assert type(Tokens().to_python()) == type(rasp.tokens)
    assert type(Equal().to_python() == type(rasp.Comparison.EQ))
    assert type(test_select_python) == type(actual_ts_python)
    
    test_select_string = test_select.str(Tokens().str(), Tokens().str(), Equal().str())
    actual_ts_string = "select(tokens, tokens, ==)"
    assert(test_select_string == actual_ts_string)
    
    
    test_aggregate = Aggregate()
    print(rasp.Aggregate(rasp.Select(rasp.tokens, rasp.tokens, rasp.Comparison.EQ), rasp.tokens)("hi"))
    
    print("all tests passed hooray!")
    
'''
ABSTRACT SYNTAX TREE
This file contains the Python class that represents programs created by our rasp synthesizer.
'''
from utils import *

class OperatorNode:
    '''
    Class to represent operator nodes (i.e., an operator and its operands) as an AST.

    Args:
        operator (object): operator object (e.g., Select, Aggregate, etc.)
        children (list): list of children nodes (operands)
    
    Example:
        select_node: OperatorNode(Select(), [Tokens(), Tokens(), Equal()])
        select_node.str() = "select(tokens, tokens, ==)"
        select_node.evaluate("hi") = [[1, 0], [0, 1]]
        select_node.to_python() = rasp.Select(rasp.tokens, rasp.tokens, rasp.Comparison.EQ)
    '''
    def __init__(self, operator, children):
        self.operator = operator
        self.children = children
        self.weight = operator.weight + sum([child.weight for child in children])
        self.return_type = operator.return_type
    
    def str(self):
        if len(self.children) != self.operator.n_args:
            raise ValueError("Improper number of arguments for operator.")
        operand_strings = [child.str() for child in self.children]
        return f"({self.operator.str(*operand_strings)})" 
        
    def evaluate(self, input=None):
        '''
        Directly evaluate the python translation.
        '''
        exe = self.to_python()
        return exe(input)

        # DEPRECATED VERSION: uses the actual rasp repl
        # exe = f"({self.str()})" + f"({repr(input)});".replace("'", "\"")
        # return run_repl(exe)
        
    def to_python(self):
        if len(self.children) != self.operator.n_args:
            raise ValueError("Improper number of arguments for operator.")  
        operands = [child.to_python() for child in self.children]
        return self.operator.to_python(*operands)
    
'''
TESTING
'''
if __name__ == "__main__":
    from python_embedded_rasp import *
    from tracr.rasp import rasp
    
    select_op = OperatorNode(Select(), [Tokens(), Tokens(), Equal()]) # wait should children be operators or operator nodes? maybe can be either?
    assert (select_op.weight == 4)
    
    select_op_str = select_op.str()
    actual_so_str = "(select(tokens, tokens, ==))"
    assert select_op_str == actual_so_str
    
    select_op_res = select_op.evaluate("hi")
    actual_so_res = [[1, 0],[0, 1]]
    assert select_op_res == actual_so_res 
    
    select_op_python = select_op.to_python()
    actual_so_python = rasp.Select(rasp.tokens, rasp.tokens, rasp.Comparison.EQ)
    assert type(select_op_python) == type(actual_so_python)
    
    print("all tests passed hooray!")
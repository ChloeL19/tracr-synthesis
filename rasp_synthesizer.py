'''
BOTTOM-UP ENUMERATIVE SYTHESIS FOR RASP

Usage:
python rasp_synthesis.py --examples
'''
import numpy as np
import argparse
import itertools
import time
import ast
import re
from tracr.compiler import compiling
from typing import get_args
import inspect

from abstract_syntax_tree import *
from python_embedded_rasp import *

# PARSE ARGUMENTS
def parse_args():
    '''
    Parse command line arguments.
    '''
    parser = argparse.ArgumentParser(description="Bottom-up enumerative synthesis for RASP.")
    parser.add_argument('--examples', required=True, help="input/output sequence examples for synthesis")
    parser.add_argument('--max_weight', type=int, required=False, default=10, help="Maximum weight of programs to consider before terminating search.")
    args = parser.parse_args()
    return args

# ANALYZE EXAMPLES
def analyze_examples(inputs):
    '''
    Returns a list of unique (input_sequence, output_sequence) tuples of proper python types.
        Ensures each example is only numeric values or only char values.
    Returns useful constants given the input examples. 
    '''
    example_ins = []
    example_outs = []
    try:
        # Safely evaluate the string to a Python object
        examples_lst = ast.literal_eval(inputs)
    except (SyntaxError, ValueError) as e:
        raise argparse.ArgumentTypeError(f"Invalid examples format: {e}")
    
    if not isinstance(examples_lst, list):
        raise ValueError("Input should be a list.")
    for ex in examples_lst:
        try:
            ins, outs = ex[0], ex[1]
        except:
            raise argparse.ArgumentTypeError(f"Invalid examples format.")
        
        def same_legal_type(lst):
            return (all(isinstance(x, int) for x in lst) or
                    all(isinstance(x, float) for x in lst) or
                    all(isinstance(x, bool) for x in lst) or
                    all(isinstance(x, str) for x in lst))
        
        if same_legal_type(ins) and same_legal_type(outs):
            example_ins.append(ins)
            example_outs.append(outs)
            continue
        raise argparse.ArgumentTypeError(f"Each example must have consistent types. Expected inputs to have type {first_in_type} and outputs to have {first_out_type} but instead inputs have types {[type(x) for x in ins]} and outputs have types {[type(x) for x in outs]}")
    
    return example_ins, example_outs
    
# GET VOCABULARY
def get_vocabulary(examples):
    '''
    Returns vocabulary for later compiling the RASP model.
    ''' 
    vocab = []  
    for ex in examples:
        ins, outs = ex[0], ex[1]
        vocab.extend([obj for obj in ins])
    return set(vocab)
    
# CHECK OBSERVATIONAL EQUIVALENCE
def check_obs_equivalence(examples, program_a, program_b):
    try:
        inputs = [example[0] for example in examples]
        a_output = None
        b_output = None
        if program_a not in rasp_consts:
            a_output = [program_a.evaluate(input) for input in inputs]
        if program_b not in rasp_consts:
            b_output = [program_b.evaluate(input) for input in inputs]
    except:
        return True # force the synthesizer to not consider this program

    return a_output == b_output

# CHECK CORRECTNESS
def check_correctness(examples, program):
    '''
    Checks if the programs output matches expected output on all examples.
    '''
    try:
        inputs = [example[0] for example in examples]
        outputs = [example[1] for example in examples]
        program_output = [program.evaluate(input) for input in inputs]
    except:
        return False
    
    print(program.str())
    print(program_output)
    
    # TODO return number that match and return this
    
    return program_output == outputs

# COMPARE TYPE SIGNATURES
def compare_types(list1, list2):
    for idx, type1 in enumerate(list1):
        if idx >= len(list2):
            return False  # The first list is longer than the second list

        type2 = list2[idx]

        # Check if type2 is a Union
        if hasattr(type2, '__origin__') and type2.__origin__ is Union:
            # Extract types from Union
            types_in_union2 = get_args(type2)
            # Check if type1 is a Union
            if hasattr(type1, '__origin__') and type1.__origin__ is Union:
                types_in_union1 = get_args(type1)
                # Check if all types in type1's Union are in type2's Union
                if not all(any(t1 == t2 for t2 in types_in_union2) for t1 in types_in_union1):
                    return False
            else:
                # Check if type1 is in type2's Union
                if not any(type1 == t2 for t2 in types_in_union2):
                    return False
        else:
            # Direct type comparison
            if type1 != type2:
                return False

    return True

# RUN SYNTHESIZER
def run_synthesizer(examples, max_weight):
    '''
    Run bottom-up enumerative synthesis.
    '''
    program_bank = rasp_consts
    program_bank_str = [p.str() for p in program_bank]
    
    # TODO: store approximate programs, measured by number of output examples that match
    
    # iterate over each level
    for weight in range(2, max_weight):
        
        for op in rasp_operators:
            combinations = itertools.permutations(program_bank, op.n_args)
            
            for combination in combinations:
                
                type_signature = [p.return_type for p in combination]
                
                if not compare_types(type_signature, op.arg_types):
                    continue
    
                if sum([p.weight for p in combination]) > weight:
                    continue
                
                program = OperatorNode(op, combination)
                
                if program.str() in program_bank_str:
                    continue
                
                if any([check_obs_equivalence(examples, program, p) for p in program_bank]):
                    continue
                
                program_bank.append(program)
                program_bank_str.append(program.str())
                
                if check_correctness(examples, program):
                    return(program)  
 
    return None

# COMPILE RASP MODEL
if __name__ == "__main__":
    
    '''
    Some examples:
    Identify anagrams:
    [[['V','I','W',',','W','I','V'], [True, True, True, True, True, True, True]],[['a','b',',','b','a'], [True, True, True, True, True]],[['e','l',',','s','t'], [False, False, False, False, False]]]
        Output: times out
    Calculate the median of a list of numbers:
    [[[1,2,3,4,5], [3,3,3,3,3]], [[2,8,10,11], [9,9,9,9]], [[1,2,3],[2,2,2]]]
        Output: times out
    Identity function:
    [[['h','i'], ['h','i']]]
        Output: (aggregate((select(tokens, tokens, ==)), tokens))
    Histogram:
    [[['h', 'e', 'l', 'l', 'o'], [1,1,2,2,1]]]
        Output: (select_width((select(tokens, tokens, ==))))
    Length:
    [[[7,2,5],[3,3,3]],[[1],[1]],[[2,0,1,7,3,6,8,20],[8,8,8,8,8,8,8,8]]]
        Output: (select_width((select(tokens, tokens, true))))
    Calculate mean of list of numbers:
    [[[5,10,3,2,43], [12.6, 12.6, 12.6, 12.6, 12.6]],[[1,2], [1.5, 1.5]],[[3,3,3],[3,3,3]]]
        Output: (aggregate((select(tokens, tokens, true)), tokens))
    Reverse a string:
    [[['h', 'i'], ['i', 'h']]]
        Output: times out
        Expected: aggregate(select(indices, (select_width((select(tokens, tokens, true)))) - indices - 1, ==), tokens);
    PERSONAL TODOS:
    - output several similar programs
    - 
    
    '''
    
    args = parse_args()
    inputs, outs = analyze_examples(args.examples)
    examples = list(zip(inputs, outs))
    print("Received the following input and output examples:")
    print(examples)
    max_seq_len = 0
    for i in inputs:
        max_seq_len = max(len(i), max_seq_len)
    vocab = get_vocabulary(examples)
    
    print("Running synthesizer with")
    print("Vocab: {}".format(vocab))
    print("Max sequence length: {}".format(max_seq_len))
    print("Max weight: {}".format(args.max_weight))
    
    program = run_synthesizer(examples, args.max_weight)
    
    if program:
        algorithm = program.to_python()
        
        bos = "BOS"
        model = compiling.compile_rasp_to_model(
            algorithm,
            vocab=vocab,
            max_seq_len=max_seq_len,
            compiler_bos=bos,
        )
        
        
        def extract_layer_number(s):
            match = re.search(r'layer_(\d+)', s)
            if match:
                return int(match.group(1)) + 1
            else:
                return None
        
        layer_num = extract_layer_number(list(model.params.keys())[-1])
        print(f"The following program has been compiled to a transformer with {layer_num} layer(s):")
        print(program.str())
    else:
        print("No program found.")
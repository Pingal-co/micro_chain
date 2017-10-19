"""
VM for a concatenative (stack-based) mini-language. Follow Postfix notation. 
Inspired by Bitcoin support of Forth-like scripting language but it is more expressive and allows adding smart contracts using python, 
Ref : http://evincarofautumn.blogspot.com/2012/02/why-concatenative-programming-matters.html
Ref : http://www.kevinalbrecht.com/code/joy-mirror/j01tut.html

Such concatenative macros should be written in Elixir, which is a full-fledged expression language. 
But, this is a super-simple expression language to test smart contracts. 
There are no statements, only expressions that compute a result and return true/false. 
Operators are not built into the language—they are ordinary functions with symbolic names.
Expressions may use infix operators with different precedences, as in many other languages. 


At a high level, postfix syntax can be thought of as representing a data flow graph.
Our blockchain store these data flow transactions (inputs, operations and outputs), 
so that lazy evaluations can be performed to verify any transaction,
or to do fold operation over the complete history

"""
from smart_contracts import constants, procedures

# store parameters and unevaluated data structures in memory
stack = []
# an abstract syntax tree or a compiled stack
ast = []


# cannot compare against the function type directly
lambdaType = type(lambda x: x) 

def output(s):
    # should send the ouput to the terminal, or anywhere else 
    print(s)

def clear(s):
    # remove from memory
    del s[:]

def is_num(x):
	try:
        float(x)
        return True
	except:
		return False    


def is_hashable(x):
	try:
		x in {}
		return True
	except:
		return False

def is_data_structure(x):
    # using deliminators \" this is a string \" \" this is a list \" 
    # every expression is just a list of commands and parameters
    return type(x) is str and len(x) > 2 and x.startswith("\"") and x.endswith("\"")

def unquote(x):
    if is_data_structure(x):
        return x[1:len(x) - 1]
    return x

def compile_word(word):
    if word == ":":
        # ast is global and mutable
        ast.append([])
        return []
    elif word == ";":
        ast[len(ast) - 2].append(ast.pop())
        return []
    elif type(word) is str and word.startswith("$"):
        # $name is a variable, previous word was value in postfix notation
        constants[word[1:]] = ast[len(ast) - 1].pop()
        return []
    elif is_num(word):
        return [float(word)]
    elif is_data_structure(word):
        return [word]
    elif is_hashable(word):
        if word in constants:
            return constants[word]
        elif word in procedures:
            return [procedures[word]]
        print("unknown word " + str(word))

def compile_expression(msg):
    # everything in a expression is a word. Each word is separated by space
    # Data structures are quoted and are a list \" [1000 >] \" : quoted data struture
    # so we can put a data structure on the stack, without evaluating it
    for word in msg.split(" "):
        w = compile_word(str(word)) 
        # put w on an abstract syntax tree or a separate stack.            
        ast[len(ast) - 1].extend(w)

def execute(compiled_ast):
    # language: everything is a expression
    # stack is for holding parameters to be passed
    for value in compiled_ast:
        if isinstance(value, float) or isinstance(value, list):
            stack.append(value)
        elif is_data_structure(value):
            stack.append(unquote(value))
        elif type(value) == lambdaType:
            value(stack)
        else:
            print("unknown word " + str(value))

# builtin stored procedures.
# A smart contract is just a stored procedure and anonymous function
procedures["."]    = lambda stack: output(stack[len(stack) - 1])
procedures[".s"]   = lambda stack: output(str(stack))
### STACK HANDLING ###
# [A] drop  ==
procedures["CMD_DROP"]  = lambda stack: stack.pop()
procedures["CMD_CLS"]  = lambda stack: clear(stack)
# [A] dup  == [A] [A]
procedures["CMD_DUP"]  = lambda stack: stack.append(stack[len(stack) - 1])
# [B] [A] swap == [A] [B]
procedures["CMD_SWAP"] = lambda stack: stack.append(stack.pop(len(stack) - 2))

### DATA STRUCTURE MATH ###
# [B] [A] cat  == [B A]
procedures["CMD_ADD"]    = lambda stack: stack.append(stack.pop() + stack.pop())
procedures["CMD_SUB"]    = lambda stack: stack.append(-(stack.pop() - stack.pop()))
procedures["CMD_MUL"]    = lambda stack: stack.append(stack.pop() * stack.pop())
procedures["CMD_DIV"]    = lambda stack: stack.append(1/(stack.pop() / stack.pop()))

### CONTROL STRUCTURE ###
# [1000 >]  [2 /]  [3 *]  ifte
procedures["CMD_IFTE"]  = lambda stack: (execute(stack.pop()) if stack.pop() else stack.pop())

### RUN ###
# [ +  20  *  10  4  - ]  i   ==  +  20  *  10  4  -
procedures["CMD_RUN"] = lambda stack: execute(stack.pop())


def main(msg):
    if len(ast) == 0:
        ast.append([])
    
    # parse the msg and make the ast
    compile_expression(msg, ast)

    # run ast and clear it
    if len(ast) == 1:
        execute(ast[0], stack)
        clear(ast)

if __name__ == '__main__':
    #while True:
    main()



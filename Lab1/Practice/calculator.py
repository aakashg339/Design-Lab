import ply.lex as lex
import ply.yacc as yacc
import sys

# List of tokens
tokens = [
    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'MODULUS',
    'POWER',
    'EQUALS',
    'DOUBLE_EQUALS',
    'LPAREN',
    'RPAREN',
 #   'POSTFIX',
 #   'PREFIX',
]

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_MODULUS = r'%'
t_POWER = r'\^'
t_DOUBLE_EQUALS = r'=='
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
#t_POSTFIX = r'postfix'
#t_PREFIX = r'prefix'
t_ignore = r' '

# Regular expression rules with some action code
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'NAME'
    return t

def t_error(t):
    print("Illegal characters")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE', 'MODULUS'),
    ('left', 'POWER'),
    ('left', 'DOUBLE_EQUALS'),
)

def p_calc(p):
    '''
    calc : expression
         | var_assign
         | empty
    '''
    print(run(p[1]))

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
    '''
    p[0] = ('=', p[1], p[3])

def p_expression_lparen_rparen(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]

def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression MODULUS expression
               | expression POWER expression
               | expression PLUS expression
               | expression MINUS expression
               | expression DOUBLE_EQUALS expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_uniaryMinus(p):
    '''
    expression : MINUS expression
    '''
    p[0] = -p[2]

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0] = p[1]

def p_expression_name(p):
    '''
    expression : NAME
    '''
    p[0] = ('var', p[1])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    print("Syntax error found!")

parser = yacc.yacc()
env = {}
def run(p):
    global env
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '%':
            return run(p[1]) % run(p[2])
        elif p[0] == '^':
            return run(p[1]) ** run(p[2])
        elif p[0] == '==':
            return run(p[1]) == run(p[2])
        elif p[0] == '=':
            env[p[1]] = run(p[2])
        elif p[0] == 'var':
            if p[1] not in env:
                return 'Undeclared variable found!'
            else:
                return env[p[1]]
    else:
        return p

# Tokenize
while True:
    # Take input expression from the user
    input_expression = input("user: ")

    if input_expression == "exit":
        sys.exit()

    parser.parse(input_expression)


from ply import lex, yacc

# Define tokens
tokens = (
    'LPAREN',
    'RPAREN',
)

# Define regular expressions for tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore  = ' /t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Define the lexer
lexer = lex.lex()

# Define the parser rules
def p_expression(p):
    '''
    expression : LPAREN expression RPAREN
               | expression LPAREN expression RPAREN
               | empty
    '''
    pass
def p_empty(p):
    'empty :'
    pass
# Error rule for syntax errors
def p_error(p):
    raise SyntaxError("Invalid Matching.")
# Build the parser
parser = yacc.yacc()

# Test the parser
string = input("Enter the String: ")
try:
   result = parser.parse(string)
   print("Valid Matching.")
except SyntaxError:
   print("Invalid Matching.")



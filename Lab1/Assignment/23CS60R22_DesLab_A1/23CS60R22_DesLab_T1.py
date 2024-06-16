import ply.lex as lex
import ply.yacc as yacc
import sys

havingLexicalError = False
havingSyntaxError = False

# Lexical part
# List of tokens
tokens = [
    'LPAREN',
    'RPAREN',
]


# Regular expression rules for simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = r' '

def t_error(t):
    global havingLexicalError
    # Find the position of the end of the line
    endLinePos = t.lexer.lexdata.find('\n', t.lexer.lexpos)
    if endLinePos == -1:
        # If there's no '\n' (end of line), skip to the end of input
        t.lexer.skip(len(t.lexer.lexdata) - t.lexer.lexpos)
    else:
        # Calculate the number of characters until the end of the line and skip
        charsTillEndLine = endLinePos - t.lexer.lexpos
        t.lexer.skip(charsTillEndLine)
    havingLexicalError = True
    # t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# printing tokens
def printTokens(input_expression):
    lexer.input(input_expression)
    while(True):
        tok = lexer.token()
        if not tok:
            break;
        print(tok.type, end =" ")
    print()

# Syntax part
# Parsing rules
precedence = (
    ('left', 'LPAREN', 'RPAREN'),
)

# def p_calc(p):
#     '''
#     calc : expression
#     '''
    #print("Valid Matching. Note: The spaces are to be ignored.")

# s-> (s)s | e

def p_expression_expression(p):
    '''
    expression : LPAREN expression RPAREN expression
    '''
    p[0] = ('(', p[1], ')', p[2])    

# def p_expression_lparen_rparen(p):
#     '''
#     expression : LPAREN expression RPAREN
#     '''
#     p[0] = ('()', p[2])

# def p_expression_lparen_rparen_terminal(p):
#     '''
#     expression : LPAREN RPAREN
#     '''
#     p[0] = (p[1], p[2])  

def p_expression_empty(p):
    '''
    expression : empty
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    global havingSyntaxError
    havingSyntaxError = True
    

parser = yacc.yacc()

# Taking input and making decisions accordingly.
while True:
    # Take input expression from the user
    input_expression = input("user: ")

    if input_expression == "exit":
        sys.exit()

    # print the tokens
    printTokens(input_expression)

    if havingLexicalError:
        print("Invalid Matching. Note: The spaces are to be ignored. Having Lexical Error.")
        havingLexicalError = False
    else:
        parser.parse(input_expression)

        if havingSyntaxError:
            print("Invalid Matching. Note: The spaces are to be ignored. Having Syntax Error.")
            havingSyntaxError = False
        else:
            print("Valid Matching. Note: The spaces are to be ignored.")
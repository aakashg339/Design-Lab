import ply.lex as lex
import ply.yacc as yacc

###DEFINING TOKENS###
tokens = ('BEGINTABLE', 
'OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF',
'CONTENT', 'OPENDATA', 'CLOSEDATA' ,'OPENSPAN',
'CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 'OPENSTYLE', 'CLOSESTYLE','GARBAGE')
t_ignore = '\t'

###############Tokenizer Rules################
def t_BEGINTABLE(t):
     r'<caption.class="infobox-title.summary">Games.of.the.XXXII.Olympiad</caption>'
     return t

def t_OPENTABLE(t):
    r'<tbody[^>]*>'
    return t

def t_CLOSETABLE(t):
    r'</tbody[^>]*>'
    return t

def t_OPENROW(t):
    r'<tr[^>]*>'
    return t

def t_CLOSEROW(t):
    r'</tr[^>]*>'
    return t

def t_OPENHEADER(t):
    r'<th[^>]*>'
    return t

def t_CLOSEHEADER(t):
    r'</th[^>]*>'
    return t

def t_OPENHREF(t):
    r'<a[^>]*>'
    return t

def t_CLOSEHREF(t):
    r'</a[^>]*>'
    return t

def t_OPENDATA(t):
    r'<td[^>]*>'
    return t

def t_CLOSEDATA(t):
    r'</td[^>]*>'
    return t

def t_CONTENT(t):
    r'[A-Za-z0-9, ]+'
    return t

def t_OPENDIV(t):
    r'<div[^>]*>'

def t_CLOSEDIV(t):
    r'</div[^>]*>'

def t_OPENSTYLE(t):
    r'<style[^>]*>'

def t_CLOSESTYLE(t):
    r'</style[^>]*>'

def t_OPENSPAN(t):
    r'<span[^>]*>'

def t_CLOSESPAN(t):
    r'</span[^>]*>'

def t_GARBAGE(t):
    r'<[^>]*>'

def t_error(t):
    t.lexer.skip(1)
####################################################################################################################################################################################################
											#GRAMMAR RULES
isOpening = True

def p_start(p):
    '''start : table'''
    print("-> start parsed")
    p[0] = p[1]

def p_skiptag(p):
    '''skiptag : CONTENT skiptag
               | OPENHREF skiptag
               | CLOSEHREF skiptag
               | empty'''

def p_handleheader(p):
    '''handleheader : OPENHEADER CONTENT CLOSEHEADER handleheader
                    | OPENHEADER CONTENT CLOSEHEADER dataCell
                    | OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER dataCell
                    | OPENHEADER CONTENT CLOSEHEADER dataCell2
                    | empty'''
    # if len(p) == 5:
    #   print(p[2], end =" ")

def p_dataCell(p):
    '''dataCell : OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA dataCell
    		    | OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA dataCell
                | OPENDATA CONTENT CLOSEDATA dataCell
                | OPENDATA CLOSEDATA dataCell
                | OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CLOSEDATA dataCell
                | OPENDATA CONTENT OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA dataCell
                | OPENDATA CONTENT CONTENT OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CLOSEDATA dataCell
                | OPENDATA CONTENT CONTENT OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA dataCell
                | OPENDATA skiptag CLOSEDATA dataCell
                | empty'''
    global isOpening
    if len(p) == 5 and p[2] is not None:
        if isOpening:
            print("Opening: ", p[2])
            isOpening = False
        else:
            print("Closing: ", p[2])
    if len(p) == 8:
        print("Host city: ",p[3], p[5])
    if len(p) == 10:
        print("Motto: ", p[2])
    if len(p) == 11:
        print("Athletes: ", p[2], '(', p[3], ')')
    if len(p) == 14:
        print("Nations: ", p[2], p[3], p[5], p[7], p[9], p[11])
 
def p_dataCell2(p):
    '''dataCell2 : OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CLOSEDATA dataCell2
                | empty'''
    if len(p) == 10:
        print("Events: ", p[2], p[4], p[6], '(',p[7], ')')

def p_handlerow(p):
    '''handlerow : OPENROW handleheader CLOSEROW handlerow 
                 | OPENROW dataCell CLOSEROW handlerow
                 | empty'''
    print("-> handlerow parsed")

def p_table(p):
    '''table : BEGINTABLE skiptag OPENTABLE handlerow '''
    print("-> table parsed")

def p_empty(p):
    '''empty :'''
    pass

def p_content(p):
    '''content : CONTENT
               | empty'''
    p[0] = p[1]
    print("-> content parsed")

def p_error(p):
    pass

#########DRIVER FUNCTION#######
def main():
    try:
        file_obj= open('webpage.html','r',encoding="utf-8")
        data=file_obj.read()
        file_obj.close()
        lexer = lex.lex()
        lexer.input(data)
        # for tok in lexer:
        #     print(tok)
        parser = yacc.yacc()
        parser.parse(data)
    except IOError:
        print("Error opening file webpage.html")

if __name__ == '__main__':
    main()
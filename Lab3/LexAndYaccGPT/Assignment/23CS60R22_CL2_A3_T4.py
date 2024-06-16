import ply.lex as lex
import ply.yacc as yacc

# To extract coaching staff details

###DEFINING TOKENS###
tokens = ('BEGINTABLE', 
'OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF',
'CONTENT', 'OPENDATA', 'CLOSEDATA' ,'OPENSPAN',
'CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 'OPENSTYLE', 'CLOSESTYLE','GARBAGE')
t_ignore = '\t'

###############Tokenizer Rules################
def t_BEGINTABLE(t):
     r'<caption>2020.Summer.Olympics.host.city.election<sup.id="cite_ref-Statesman-AP_25-0".class="reference"><a.href=".cite_note-Statesman-AP-25">&.91;21&.93;</a></sup>'
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





# LexToken(OPENDATA,'<td>',1,7003)
# LexToken(CONTENT,'Physiotherapist',1,7007)
# LexToken(CLOSEDATA,'</td>',1,7023)
# LexToken(OPENDATA,'<td>',1,7029)
# LexToken(CONTENT,'vacant',1,7033)
# LexToken(OPENHREF,'<a href="#cite_note-SLMirror-87">',1,7090)
# LexToken(CONTENT,'91',1,7125)
# LexToken(CONTENT,'87',1,7128)
# LexToken(CONTENT,'93',1,7132)
# LexToken(CLOSEHREF,'</a>',1,7135)
# LexToken(CLOSEDATA,'</td>',1,7146)

# 



def p_start(p):
    '''start : table'''
    p[0] = p[1]

def p_skiptag(p):
    '''skiptag : CONTENT skiptag
               | OPENHREF skiptag
               | CLOSEHREF skiptag
               | empty'''

def p_handleheader(p):
    '''handleheader : OPENHEADER CONTENT CLOSEHEADER handleheader
                    | empty'''
    #if len(p) == 5:
    #    print("Header: ", p[2])

def p_dataCell(p):
    '''dataCell : OPENDATA CONTENT CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA empty
                | OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CONTENT OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA empty
                | OPENDATA CONTENT CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA empty
                | OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA empty
                | OPENDATA CONTENT CLOSEDATA OPENDATA OPENHREF CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA empty
                | OPENDATA CONTENT CLOSEDATA OPENDATA CLOSEDATA empty
                | OPENDATA CONTENT OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA empty
                | OPENDATA CONTENT CLOSEDATA OPENDATA OPENHREF CLOSEHREF CONTENT CLOSEDATA empty
                | OPENDATA CONTENT CLOSEDATA OPENDATA OPENHREF CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CONTENT CONTENT CLOSEHREF skiptag CLOSEDATA empty
                | OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA empty
                '''
    # print(len(p))
    
    if len(p) == 15 and 'href' not in p[3] :
        print(p[6])
        return
    if len(p) == 14:
        if p[6] is not None:
            print(p[5], p[6])
        else:
            print(p[5])
        return
    if len(p) == 10:
        if "</a>" in p[6]:
            print(p[7])
        else:
            print(p[6])
        return
    if len(p) == 8:
        print(p[5])
        return
    if len(p) == 13:
        if 'href' in p[6]:
            return
        if p[9] != "vacant":
            print(p[9])
        return
    if len(p) == 15 :
        print(p[11])
        return
    if len(p) == 18:
        print(p[9])
    if len(p) == 23:
        print(p[9])
    if len(p) == 19:
        print(p[9])

def p_handlerow(p):
    '''handlerow : OPENROW handleheader CLOSEROW handlerow 
                 | OPENROW dataCell CLOSEROW handlerow
                 | empty'''

def p_table(p):
    '''table : OPENTABLE handlerow CLOSETABLE'''

def p_empty(p):
    '''empty :'''
    pass

def p_content(p):
    '''content : CONTENT
               | empty'''
    p[0] = p[1]

def p_error(p):
    pass

#########DRIVER FUNCTION#######
def main():
    try:
        file_obj= open('webpage.html','r',encoding="utf-8")
        data=file_obj.read()
        file_obj.close()
    except:
        print("Error. Unable to find webpage.html")
        return

    # Building lexer
    lexer = lex.lex()
    lexer.input(data)

    # Writing tokens to file
    file_obj = open('tokens.txt', 'w')
    for tok in lexer:
        # print(tok)
        file_obj.write(str(tok))
        file_obj.write('\n')
    file_obj.close()
    parser = yacc.yacc()
    parser.parse(data)

if __name__ == '__main__':
    main()
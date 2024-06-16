import ply.lex as lex
import ply.yacc as yacc

# To extract current set of icc rankings

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





# LexToken(OPENROW,'<tr>',1,64859)
# LexToken(OPENHEADER,'<th scope="row" class="infobox-label">',1,64863)
# LexToken(OPENHREF,'<a href="/wiki/ICC_Men%27s_Test_Team_Rankings" title="ICC Men&#39;s Test Team Rankings">',1,64901)
# LexToken(CONTENT,'Test',1,64989)
# LexToken(CLOSEHREF,'</a>',1,64993)
# LexToken(CLOSEHEADER,'</th>',1,64997)
# LexToken(OPENDATA,'<td class="infobox-data infobox-data-a">',1,65002)
# LexToken(CONTENT,'4th',1,65043)
# LexToken(CLOSEDATA,'</td>',1,65046)
# LexToken(OPENDATA,'<td class="infobox-data infobox-data-b">',1,65051)
# LexToken(CONTENT,'1st ',1,65092)
# LexToken(CONTENT,'1 January 1969',1,65104)
# LexToken(CLOSEDATA,'</td>',1,65127)
# LexToken(CLOSEROW,'</tr>',1,65132)
# OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA


####################################################################################################################################################################################################
											#GRAMMAR RULES
def p_start(p):
    '''start : dataCell'''
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
    '''dataCell : OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENDATA CONTENT CLOSEDATA empty
                | OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA empty
                '''
    # print(len(p))
    
    if len(p) == 10:
        print(p[3], " : ", p[7])
    if len(p) == 12:
        print(p[3], " : ", p[8])

def p_handlerow(p):
    '''handlerow : OPENROW handleheader CLOSEROW handlerow 
                 | OPENROW dataCell CLOSEROW handlerow
                 | empty'''

def p_table(p):
    '''table : BEGINTABLE skiptag OPENTABLE handlerow '''

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

    lexer = lex.lex()
    lexer.input(data)

    print("ICC Rankings:")
    
    # # Writing tokens to a file
    # file_obj = open('tokens.txt','w')
    # for tok in lexer:
    #     #print(tok)
    #     file_obj.write(str(tok)+'\n')
    # file_obj.close()
    parser = yacc.yacc()
    parser.parse(data)

if __name__ == '__main__':
    main()
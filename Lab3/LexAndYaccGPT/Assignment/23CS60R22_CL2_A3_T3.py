import ply.lex as lex
import ply.yacc as yacc

# To extract contracted players details

###DEFINING TOKENS###
tokens = ('BEGINTABLE', 
'OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF',
'CONTENT', 'OPENDATA', 'CLOSEDATA' ,'OPENSPAN','BOPEN', 'BCLOSE',
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

def t_BOPEN(t):
    r'<b[^>]*>'
    return t

def t_BCLOSE(t):
    r'</b[^>]*>'
    return t

def t_GARBAGE(t):
    r'<[^>]*>'

def t_error(t):
    t.lexer.skip(1)

# LexToken(OPENDATA,'<td>',1,224571)
# LexToken(OPENHREF,'<a href="/wiki/Temba_Bavuma" title="Temba Bavuma">',1,224575)
# LexToken(CONTENT,'Temba Bavuma',1,224625)
# LexToken(CLOSEHREF,'</a>',1,224637)
# LexToken(CLOSEDATA,'</td>',1,224641)
# LexToken(OPENDATA,'<td>',1,224647)
# LexToken(CONTENT,'33',1,224683)
# LexToken(CLOSEDATA,'</td>',1,224685)
# LexToken(OPENDATA,'<td>',1,224691)
# LexToken(CONTENT,'Right',1,224695)
# LexToken(CONTENT,'handed',1,224701)
# LexToken(CLOSEDATA,'</td>',1,224707)
# LexToken(OPENDATA,'<td>',1,224713)
# LexToken(CONTENT,'Right',1,224717)
# LexToken(CONTENT,'arm ',1,224723)
# LexToken(OPENHREF,'<a href="/wiki/Fast_bowling" title="Fast bowling">',1,224727)
# LexToken(CONTENT,'medium',1,224777)
# LexToken(CLOSEHREF,'</a>',1,224783)
# LexToken(CLOSEDATA,'</td>',1,224787)
# LexToken(OPENDATA,'<td>',1,224793)
# LexToken(OPENHREF,'<a href="/wiki/Highveld_Lions_cricket_team" class="mw-redirect" title="Highveld Lions cricket team">',1,224797)
# LexToken(CONTENT,'Lions',1,224897)
# LexToken(CLOSEHREF,'</a>',1,224902)
# LexToken(CLOSEDATA,'</td>',1,224906)
# LexToken(OPENDATA,'<td>',1,224912)
# LexToken(CONTENT,'Test, ODI, T20I',1,224916)
# LexToken(CLOSEDATA,'</td>',1,224931)
# LexToken(OPENDATA,'<td>',1,224937)
# LexToken(CONTENT,'Y',1,224941)
# LexToken(CLOSEDATA,'</td>',1,224942)
# LexToken(OPENDATA,'<td>',1,224948)
# LexToken(CONTENT,'11',1,224952)
# LexToken(CLOSEDATA,'</td>',1,224954)
# LexToken(OPENDATA,'<td>',1,224960)
# LexToken(CONTENT,'ODI ',1,224964)
# LexToken(CONTENT,'C',1,224969)
# LexToken(CLOSEDATA,'</td>',1,224971)
# LexToken(OPENDATA,'<td>',1,224977)
# LexToken(OPENHREF,'<a href="/wiki/India_national_cricket_team" title="India national cricket team">',1,225051)
# LexToken(CLOSEHREF,'</a>',1,225559)
# LexToken(CONTENT,' 2023',1,225577)
# LexToken(CLOSEDATA,'</td>',1,225582)
# LexToken(OPENDATA,'<td>',1,225588)
# LexToken(OPENHREF,'<a href="/wiki/Australia_national_cricket_team" title="Australia national cricket team">',1,225662)
# LexToken(CLOSEHREF,'</a>',1,226318)
# LexToken(CONTENT,' 2023',1,226336)
# LexToken(CLOSEDATA,'</td>',1,226341)
# LexToken(OPENDATA,'<td>',1,226347)
# LexToken(OPENHREF,'<a href="/wiki/Australia_national_cricket_team" title="Australia national cricket team">',1,226421)
# LexToken(CLOSEHREF,'</a>',1,227077)
# LexToken(CONTENT,' 2023',1,227095)
# LexToken(CLOSEDATA,'</td>',1,227101)
# | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA content CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA CLOSEROW CLOSEROW empty
                


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
    '''dataCell : OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA content skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA content CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA CLOSEROW empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA content CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA CLOSEROW empty
                | OPENDATA BOPEN OPENHREF CONTENT CLOSEHREF BCLOSE CLOSEDATA OPENDATA CONTENT CLOSEDATA empty
                '''
    # print(p[3], p[22], len(p)) # India
    # print(p[3], p[29], len(p)) # Australia
    # print(p[3], p[19], len(p)) # England
    # print(p[4]) # New Zealand
    # print(p[3], p[22], len(p)) # South Africa
    
    # Australia
    if len(p) == 45 and p[29] is not None and p[29] == "Y":
        print(p[3])
        return

    # India, Pakistan
    if len(p) == 45 and p[22] is not None and p[22] in ["A+", "A", "B", "C", "D"]:
        print(p[3])
        return
    
    # England
    if len(p) == 41 and p[19] is not None and p[19] in ["C", "D"]:
        print(p[3])
        return
    
    # New Zealand
    if len(p) == 12:
        print(p[4])
        return
    
    # South Africa
    if len(p) == 41 and p[22] is not None and p[22] == "Y":
        print(p[3], p[22])
        return

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
    except IOError:
        print("File not found or path is incorrect")
        return
    
    lexer = lex.lex()
    lexer.input(data)

    # writing tokens to file
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
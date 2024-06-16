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

# LexToken(OPENROW,'<tr>',1,1049)
# LexToken(OPENDATA,'<td>',1,1054)
# LexToken(OPENHREF,'<a href="/wiki/Temba_Bavuma" title="Temba Bavuma">',1,1058)
# LexToken(CONTENT,'Temba Bavuma',1,1108)
# LexToken(CLOSEHREF,'</a>',1,1120)
# LexToken(CLOSEDATA,'</td>',1,1124)
# LexToken(OPENDATA,'<td>',1,1130)
# LexToken(CONTENT,'33',1,1166)
# LexToken(CLOSEDATA,'</td>',1,1168)
# LexToken(OPENDATA,'<td>',1,1174)
# LexToken(CONTENT,'Right',1,1178)
# LexToken(CONTENT,'handed',1,1184)
# LexToken(CLOSEDATA,'</td>',1,1190)
# LexToken(OPENDATA,'<td>',1,1196)
# LexToken(CONTENT,'Right',1,1200)
# LexToken(CONTENT,'arm ',1,1206)
# LexToken(OPENHREF,'<a href="/wiki/Fast_bowling" title="Fast bowling">',1,1210)
# LexToken(CONTENT,'medium',1,1260)
# LexToken(CLOSEHREF,'</a>',1,1266)
# LexToken(CLOSEDATA,'</td>',1,1270)
# LexToken(OPENDATA,'<td>',1,1276)
# LexToken(OPENHREF,'<a href="/wiki/Highveld_Lions_cricket_team" class="mw-redirect" title="Highveld Lions cricket team">',1,1280)
# LexToken(CONTENT,'Lions',1,1380)
# LexToken(CLOSEHREF,'</a>',1,1385)
# LexToken(CLOSEDATA,'</td>',1,1389)
# LexToken(OPENDATA,'<td>',1,1395)
# LexToken(CONTENT,'Test, ODI, T20I',1,1399)
# LexToken(CLOSEDATA,'</td>',1,1414)
# LexToken(OPENDATA,'<td>',1,1420)
# LexToken(CONTENT,'Y',1,1424)
# LexToken(CLOSEDATA,'</td>',1,1425)
# LexToken(OPENDATA,'<td>',1,1431)
# LexToken(CONTENT,'11',1,1435)
# LexToken(CLOSEDATA,'</td>',1,1437)
# LexToken(OPENDATA,'<td>',1,1443)
# LexToken(CONTENT,'ODI ',1,1447)
# LexToken(CONTENT,'C',1,1452)
# LexToken(CLOSEDATA,'</td>',1,1454)
# LexToken(OPENDATA,'<td>',1,1460)
# LexToken(OPENHREF,'<a href="/wiki/India_national_cricket_team" title="India national cricket team">',1,1534)
# LexToken(CLOSEHREF,'</a>',1,2042)
# LexToken(CONTENT,' 2023',1,2060)
# LexToken(CLOSEDATA,'</td>',1,2065)
# LexToken(OPENDATA,'<td>',1,2071)
# LexToken(OPENHREF,'<a href="/wiki/Australia_national_cricket_team" title="Australia national cricket team">',1,2145)
# LexToken(CLOSEHREF,'</a>',1,2801)
# LexToken(CONTENT,' 2023',1,2819)
# LexToken(CLOSEDATA,'</td>',1,2824)
# LexToken(OPENDATA,'<td>',1,2830)
# LexToken(OPENHREF,'<a href="/wiki/Australia_national_cricket_team" title="Australia national cricket team">',1,2904)
# LexToken(CLOSEHREF,'</a>',1,3560)
# LexToken(CONTENT,' 2023',1,3578)
# LexToken(CLOSEDATA,'</td>',1,3584)

                


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
                | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA content CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA CLOSEROW empty
                | OPENDATA BOPEN OPENHREF CONTENT CLOSEHREF BCLOSE CLOSEDATA OPENDATA CONTENT CLOSEDATA empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA content skiptag CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA content CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA OPENDATA skiptag CLOSEDATA CLOSEROW empty
                '''
    # print(p[3], p[22], len(p)) # India
    # print(p[3], p[29], len(p)) # Australia
    # print(p[3], p[19], len(p)) # England
    # print(p[4]) # New Zealand
    # print(p[3], p[26], len(p)) # South Africa
    
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
    if len(p) == 41 and p[22] is not None and p[22].strip() == "Y":
        print(p[3])
        return
    
    # Sri Lanka
    if len(p) == 45 and p[26] is not None:
        print(p[3])
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

    # # writing tokens to file
    # file_obj = open('tokens.txt', 'w')
    # for tok in lexer:
    #     # print(tok)
    #     file_obj.write(str(tok))
    #     file_obj.write('\n')
    # file_obj.close()
    parser = yacc.yacc()
    parser.parse(data)

if __name__ == '__main__':
    main()
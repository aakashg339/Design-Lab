import ply.lex as lex
import ply.yacc as yacc

# To extract stadium details

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





# LexToken(OPENDATA,'<td>',1,171440)
# LexToken(OPENHREF,'<a href="/wiki/Melbourne_Cricket_Ground" title="Melbourne Cricket Ground">',1,171444)
# LexToken(CONTENT,'Melbourne Cricket Ground',1,171518)
# LexToken(CLOSEHREF,'</a>',1,171542)
# LexToken(CLOSEDATA,'</td>',1,171547)
# LexToken(OPENDATA,'<td>',1,171553)
# LexToken(OPENHREF,'<a href="/wiki/Melbourne" title="Melbourne">',1,171557)
# LexToken(CONTENT,'Melbourne',1,171601)
# LexToken(CLOSEHREF,'</a>',1,171610)
# LexToken(CLOSEDATA,'</td>',1,171615)
# LexToken(OPENDATA,'<td>',1,171621)
# LexToken(CONTENT,'100,024',1,171625)
# LexToken(CLOSEDATA,'</td>',1,171633)




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
    '''dataCell : OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA content CLOSEDATA OPENDATA content content CLOSEDATA OPENDATA content CLOSEDATA OPENDATA content CLOSEDATA OPENDATA content CLOSEDATA empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA content CLOSEDATA OPENDATA content content CLOSEDATA OPENDATA content CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA content CLOSEDATA empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT openhref content content content closehref CLOSEDATA OPENDATA CONTENT openhref content content content closehref CLOSEDATA OPENDATA CONTENT openhref content content content closehref CLOSEDATA empty
                | OPENDATA OPENHREF CONTENT content content CLOSEHREF CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT openhref content content content closehref CLOSEDATA OPENDATA CONTENT openhref content content content closehref CLOSEDATA OPENDATA CONTENT openhref content content content closehref CLOSEDATA empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT openhref content content content closehref CLOSEDATA OPENDATA CONTENT openhref content content content closehref CLOSEDATA OPENDATA CONTENT openhref content content content closehref CLOSEDATA empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA empty
                '''
    print(p[3])

    if len(p) == 31:
        message = "Ground: " + p[3] + ' | ' + "City: " + p[7] + ' | ' + 'Representative team: ' + p[11] + ' | '
        if p[15] is not None:
            message += 'Capacity: ' + p[15] + ' | '
        else:
            message += 'Capacity: ' + '-' + ' | '
        if p[18] is not None:
            if p[19] is not None:
                message += 'Years Used: ' + p[18] + '-' + p[19] + ' | '
            else:
                message += 'Years Used: ' + p[18] + ' | '
        else:
            message += 'Years Used: ' + '-' + ' | '
        if p[22] is not None:
            message += 'Test: ' + p[22] + ' | '
        else:
            message += 'Test: ' + '-' + ' | '
        if p[25] is not None:
            message += 'ODI: ' + p[25] + ' | '
        else:
            message += 'ODI: ' + '-' + ' | '
        if p[28] is not None:
            message += 'T20I: ' + p[28] + ' | '
        else:
            message += 'T20I: ' + '-' + ' | '
        
        print(message)

        # print("Ground: ", p[3], '|', "City: ", p[7], '|', 'Representative team: ', p[11], '|', 'Capacity: ', p[15], '|', 'First match: ', p[19], '|', 'Last match: ', p[23], '|', 'Matches: ', p[27], '|', 'Matches: ', p[28])
    if len(p) == 29:
        message = "Ground: " + p[3] + ' | ' + "City: " + p[7] + ' | ' + 'Representative team: ' + p[10] + ' | '
        if p[13] is not None:
            message += 'Capacity: ' + p[13] + ' | '
        else:
            message += 'Capacity: ' + '-' + ' | '
        if p[16] is not None:
            if p[17] is not None:
                message += 'Years Used: ' + p[16] + '-' + p[17] + ' | '
            else:
                message += 'Years Used: ' + p[16] + ' | '
        else:
            message += 'Years Used: ' + '-' + ' | '
        if p[20] is not None:
            message += 'Test: ' + p[20] + ' | '
        else:
            message += 'Test: ' + '-' + ' | '
        if p[23] is not None:
            message += 'ODI: ' + p[23] + ' | '
        else:
            message += 'ODI: ' + '-' + ' | '
        if p[26] is not None:
            message += 'T20I: ' + p[26] + ' | '
        else:
            message += 'T20I: ' + '-' + ' | '
        
        print(message)

    if len(p) == 42:
        message = "Ground: " + p[3] + ' | ' + "City: " + p[8] + ' | ' + 'Capacity: ' + p[12] + ' | ' + 'First Used: ' + p[15] + ' | ' + 'Test: ' + p[18] + ' | ' + 'ODI: ' + p[26] + ' | ' + 'T20I: ' + p[34] + ' | '
        print(message)
    
    if len(p) == 44:
        if p[4] is not None and p[5] is not None:
            message = "Ground: " + p[3] + p[4] + p[5] + ' | ' + "City: " + p[10] + ' | ' + 'Capacity: ' + p[14] + ' | ' + 'First Used: ' + p[17] + ' | ' + 'Test: ' + p[20] + ' | ' + 'ODI: ' + p[28] + ' | ' + 'T20I: ' + p[36] + ' | '
            print(message)
        elif p[4] is not None and p[5] is None:
            message = "Ground: " + p[3] + p[4] + ' | ' + "City: " + p[10] + ' | ' + 'Capacity: ' + p[14] + ' | ' + 'First Used: ' + p[17] + ' | ' + 'Test: ' + p[20] + ' | ' + 'ODI: ' + p[28] + ' | ' + 'T20I: ' + p[36] + ' | '
            print(message)
        elif p[4] is None and p[5] is None:
            message = "Ground: " + p[3] + ' | ' + "City: " + p[10] + ' | ' + 'Capacity: ' + p[14] + ' | ' + 'First Used: ' + p[17] + ' | ' + 'Test: ' + p[20] + ' | ' + 'ODI: ' + p[28] + ' | ' + 'T20I: ' + p[36] + ' | '
            print(message)
    
    if len(p) == 46:
        if p[4] is not None and p[5] is not None and p[14] is not None:
            message = "Ground: " + p[3] + ' | ' + "City: " + p[8] + ' ' + p[12] + ' | ' + 'Capacity: ' + p[16] + ' | ' + 'First Used: ' + p[19] + ' | ' + 'Test: ' + p[22] + ' | ' + 'ODI: ' + p[30] + ' | ' + 'T20I: ' + p[38] + ' | '
            print(message)
    
    if len(p) == 36:
        print("Ground: ", p[3], '|', "City: ", p[13], '|', 'First Used: ', p[17], '|', 'Last Used: ', p[20], '|', 'Test: ', p[23], '|', 'ODI: ', p[26], '|', 'T20I: ', p[29], '|', 'Total :', p[32])

    # Australia
    if len(p) == 15:
        print("Ground: ", p[3], '|', "City: ", p[8], '|', 'Capacity: ', p[12])

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

def p_openhref(p):
    '''openhref : OPENHREF
               | empty'''
    p[0] = p[1]

def p_CLOSEHREF(p):
    '''closehref : CLOSEHREF
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
        print("Error occured while opening webpage.html")
        return
    
    lexer = lex.lex()
    lexer.input(data)

    # Writing tokens to file tokens.txt
    file_obj= open('tokens.txt','w',encoding="utf-8")
    for tok in lexer:
        # print(tok)
        file_obj.write(str(tok)+'\n')
    file_obj.close()

    parser = yacc.yacc()
    parser.parse(data)

if __name__ == '__main__':
    main()
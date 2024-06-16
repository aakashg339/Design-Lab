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



# LexToken(OPENDATA,'<td>',1,392)
# LexToken(OPENHREF,'<a href="/wiki/Albion_Sports_Complex" title="Albion Sports Complex">',1,396)
# LexToken(CONTENT,'Albion Sports Complex',1,464)
# LexToken(CLOSEHREF,'</a>',1,485)
# LexToken(CLOSEDATA,'</td>',1,489)
# LexToken(OPENDATA,'<td>',1,495)
# LexToken(OPENHREF,'<a href="/wiki/Albion,_Guyana" title="Albion, Guyana">',1,499)
# LexToken(CONTENT,'Albion',1,553)
# LexToken(CLOSEHREF,'</a>',1,559)
# LexToken(CLOSEDATA,'</td>',1,563)
# LexToken(OPENDATA,'<td>',1,569)
# LexToken(CONTENT,'Guyana',1,573)
# LexToken(CLOSEDATA,'</td>',1,579)
# LexToken(OPENDATA,'<td>',1,585)
# LexToken(CONTENT,'15,000',1,589)
# LexToken(CLOSEDATA,'</td>',1,595)
# LexToken(OPENDATA,'<td>',1,601)
# LexToken(CONTENT,'1977',1,605)
# LexToken(CLOSEDATA,'</td>',1,609)
# LexToken(OPENDATA,'<td>',1,615)
# LexToken(CLOSEDATA,'</td>',1,620)
# LexToken(OPENDATA,'<td>',1,626)
# LexToken(CONTENT,'5',1,630)
# LexToken(CLOSEDATA,'</td>',1,631)
# LexToken(OPENDATA,'<td>',1,637)
# LexToken(CONTENT,'0',1,641)
# LexToken(CLOSEDATA,'</td>',1,642)
# LexToken(OPENDATA,'<td>',1,648)
# LexToken(OPENHREF,'<a href="#cite_note-35">',1,692)
# LexToken(CONTENT,'91',1,718)
# LexToken(CONTENT,'34',1,721)
# LexToken(CONTENT,'93',1,725)
# LexToken(CLOSEHREF,'</a>',1,728)
# LexToken(CLOSEDATA,'</td>',1,739)





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
                | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA CLOSEROW empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA content CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA content CLOSEDATA OPENDATA content CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA skiptag CLOSEDATA empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA content CLOSEDATA OPENDATA content CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA skiptag CLOSEDATA empty
                '''
    # print(p[3], len(p))

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
    if len(p) == 16:
        print("Ground: ", p[3], '|', "City: ", p[8], '|', 'Capacity: ', p[12])
    
    # Pa
    if len(p) == 35:
        print("Ground: ", p[3], '|', "City: ", p[13], '|', 'First Used: ', p[17], '|', 'Last Used: ', p[20], '|', 'Test: ', p[23], '|', 'ODI: ', p[26], '|', 'T20I: ', p[29], '|', 'Total :', p[32])

    # West
    if len(p) == 33:
        print("Ground: ", p[3], '|', "City: ", p[8], '|', 'Country: ', p[12], '|', 'Capacity: ', str(p[15] or ''), '|', 'First Match: ', p[18], '|', 'Test: ', str(p[21] or ''), '|', 'ODI: ', str(p[24] or ''), '|', 'T20I: ', p[27])

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

    # # Writing tokens to file tokens.txt
    # file_obj= open('tokens.txt','w',encoding="utf-8")
    # for tok in lexer:
    #     # print(tok)
    #     file_obj.write(str(tok)+'\n')
    # file_obj.close()

    parser = yacc.yacc()
    parser.parse(data)

if __name__ == '__main__':
    main()
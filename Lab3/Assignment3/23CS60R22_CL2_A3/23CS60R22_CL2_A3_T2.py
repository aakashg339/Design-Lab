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





# LexToken(OPENHEADER,'<th style="width:6em; padding-right:1em">',1,48394)
# LexToken(CONTENT,'Catches',1,48435)
# LexToken(OPENHREF,'<a href="/wiki/Stumped" title="Stumped">',1,48443)
# LexToken(CONTENT,'stumpings',1,48483)
# LexToken(CLOSEHREF,'</a>',1,48492)
# LexToken(CLOSEHEADER,'</th>',1,48496)
# LexToken(OPENDATA,'<td>',1,48502)
# LexToken(CONTENT,'9',1,48506)
# LexToken(CLOSEDATA,'</td>',1,48509)
# LexToken(OPENDATA,'<td>',1,48515)
# LexToken(CONTENT,'1',1,48519)
# LexToken(CLOSEDATA,'</td>',1,48522)
# LexToken(OPENDATA,'<td>',1,48528)
# LexToken(CONTENT,'13',1,48532)
# LexToken(CLOSEDATA,'</td>',1,48536)
# LexToken(OPENDATA,'<td>',1,48542)
# LexToken(CONTENT,'53',1,48546)
# LexToken(CLOSEDATA,'</td>',1,48550)



roleFlag = True
matchesDone = False
runsScored = False
bestBowling = False
bowlingAverage = False
i = 0

def p_start(p):
    '''start : dataCell
             '''
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
    '''dataCell : OPENHEADER CONTENT CLOSEHEADER OPENDATA CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA empty
                | OPENHEADER CONTENT CLOSEHEADER OPENDATA CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CLOSEDATA empty
                | OPENHEADER CONTENT CLOSEHEADER OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA empty
                | OPENHEADER CONTENT CONTENT CLOSEHEADER OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA empty
                | OPENHEADER CONTENT CLOSEHEADER OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA empty
                | OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENDATA CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CONTENT CLOSEDATA empty
                | OPENHEADER CONTENT CONTENT CLOSEHEADER OPENDATA CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CONTENT CLOSEDATA empty
                | OPENHEADER CONTENT CLOSEHEADER OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA empty
                | OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER OPENDATA CONTENT CLOSEDATA OPENDATA CLOSEDATA OPENDATA CLOSEDATA OPENDATA CONTENT CLOSEDATA empty
                | OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENDATA CONTENT CLOSEDATA OPENDATA CLOSEDATA OPENDATA CLOSEDATA OPENDATA CONTENT CLOSEDATA empty
                | OPENHEADER CONTENT CLOSEHEADER OPENDATA CONTENT CONTENT CLOSEDATA OPENDATA CLOSEDATA OPENDATA CLOSEDATA OPENDATA CONTENT CONTENT CLOSEDATA empty
                | OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENDATA CONTENT CONTENT CLOSEDATA OPENDATA CLOSEDATA OPENDATA CLOSEDATA OPENDATA CONTENT CONTENT CLOSEDATA empty
                | OPENHEADER CONTENT CLOSEHEADER OPENDATA CONTENT CLOSEDATA OPENDATA CLOSEDATA OPENDATA CLOSEDATA OPENDATA CONTENT CLOSEDATA empty
                | OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA empty
                '''
    
    global roleFlag
    global matchesDone
    global runsScored
    global bestBowling
    global bowlingAverage
    global i

    if len(p) == 28:
        print("Date of Birth: ", p[10])
        return
    if len(p) == 42:
        print("National side: ", p[35])
        return
    if len(p) == 10 and roleFlag == True:
        print("Role: ", p[6])
        roleFlag = False
        return
    if len(p) == 11:
        print("Domstic Team Information: ", p[2] + '-' + p[3], p[7])
        return
    if len(p) == 10 and roleFlag == False:
        print("Domstic Team Information: ", p[2], p[6])
        return
    # Matches
    if len(p) == 17 and matchesDone == False:
        print(p[2] + ': ', p[5], p[8], p[11], p[14])
        matchesDone = True
        return
    # Runs scored
    if len(p) == 17 and matchesDone == True and runsScored == False:
        print(p[2] + ': ', p[5], p[8], p[11], p[14])
        runsScored = True
        return
    # Batting Average
    if len(p) == 23:
        print(p[3] + ': ', p[7] + '.' + p[8], p[11] + '.' + p[12], p[15] + '.' + p[16], p[19] + '.' + p[20])
        return
    # 100s/50s
    if len(p) == 22:
        print(p[2] + '/' + p[3] + ': ', p[6] + '/' + p[7], p[10] + '/' + p[11], p[14] + '/' + p[15], p[18] + '/' + p[19])
        return
    # Top Score
    if len(p) == 19 and bowlingAverage == False:
        print(p[2]  + ': ', p[5], p[8], p[11], p[16])
        bowlingAverage = True
        return
    # Balls bowled
    if len(p) == 18:
        print(p[3] +  p[5] + ': ', p[8], '-', '-', p[15])
        return
    # Wickets, 5 wickets in innings
    if len(p) == 17 and matchesDone == True and runsScored == True and bestBowling == False:
        print(p[3] + ': ', p[7], '-', '-', p[14])
        i = i+1
        if i == 2:
            bestBowling = True
        return
    # Bowling Average
    if len(p) == 19 and bowlingAverage == True:
        print(p[3] + ': ', p[7] + '.' + p[8], '-', '-', p[15] + '.' + p[16])
        bowlingAverage = False
        return
    # Best Bowling
    if len(p) == 17 and matchesDone == True and runsScored == True and bestBowling == True:
        print(p[2] + ": ", p[5] + '/' + p[6], '-', '-', p[13] + '/' + p[14])
        return
    # 10 wickets in match
    if len(p) == 15:
        print(p[2] + ': ', p[5], '-', '-', p[12])
        return
    # Catches/Stumpings
    if len(p) == 20:
        print(p[2] + '/' + p[4] + ': ', p[8] + '/–', p[11] + '/–', p[14] + '/–', p[17] + '/–')
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
    global parsedData
    global eachRowData
    try:
        file_obj= open('webpage_player.html','r',encoding="utf-8")
        data=file_obj.read()
        file_obj.close()
    except:
        print("Error opening file 'webpage.html'")
        return
    
    lexer = lex.lex()
    lexer.input(data)
    # # write tokens to file
    # try:
    #     file_obj = open('tokens.txt', 'w')
    #     for tok in lexer:
    #         #print(tok)
    #         file_obj.write(str(tok))
    #         file_obj.write('\n')
    #     file_obj.close()
    # except:
    #     print("Error opening file 'tokens.txt'")
    #     return

    parser = yacc.yacc()
    parser.parse(data)


if __name__ == '__main__':
    main()
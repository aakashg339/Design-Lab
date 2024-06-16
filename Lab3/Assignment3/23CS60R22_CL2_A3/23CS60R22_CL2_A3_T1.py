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
parsedData = []
eachRowData = []

def p_start(p):
    '''start : dataCell'''
    p[0] = p[1]



# '''dataCell : OPENTABLE OPENROW OPENDATA CONTENT CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA CLOSEROW  CLOSETABLE empty
#                 | OPENROW OPENDATA CONTENT CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA CLOSEROW empty
#                 | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
#                 | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
#                 | OPENTABLE OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA CLOSEROW CLOSETABLE empty'''


def p_dataCell(p):
    '''dataCell : OPENROW OPENDATA CONTENT CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA CONTENT CONTENT CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CONTENT OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA CLOSEROW
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CONTENT CONTENT CONTENT CONTENT CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA OPENHREF CONTENT CONTENT CLOSEHREF CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA CLOSEROW empty
                | OPENROW OPENDATA CLOSEDATA CLOSEROW empty
                '''
    # Top - 3
    # Middle - 11
    # Bottom - 0

    # Dates 70
    
    global eachRowData

    # For left table
    if len(p) == 11 and p[4].strip() != '': # In
        eachRowData = [-1,-1,-1, -1]
        eachRowData[1] = p[3].strip() + '-' + p[4].strip()
        # print("Date: ", p[3].strip(), '-', p[4].strip())
        return
    if len(p) == 7: # In
        eachRowData = [-1,-1,-1, -1]
        eachRowData[1] = p[3].strip()
        # print("Date: ", p[3])
        return
    if len(p) == 8: # In
        eachRowData = [-1,-1,-1, -1]
        eachRowData[1] = p[3].strip() + '/' + p[4].strip()
        # print("Date: ", p[3] + '/' + p[4])
        return

    # For middle table
    if len(p) == 42: # In
        # print("Match: " + p[4] + " v " + p[27])
        # print("Details: " + p[4], p[8] + '/' + p[9], p[14], p[17], p[18] + '.' + p[19], p[27], p[30], p[31] + '.' + p[32], p[35] + '/' + p[36], p[37] + '.' + p[38])
        eachRowData[0] = p[4].strip() + " v " + p[27].strip()
        eachRowData[2] = p[4].strip() + ', ' + p[8].strip() + '/' + p[9].strip() + ', ' + p[14].strip() + ', ' + p[17].strip() + ', ' + p[18].strip() + '.' + p[19].strip() + ', ' + p[27].strip() + ', ' + p[30].strip() + ', ' + p[31].strip() + '.' + p[32].strip() + ', ' + p[35].strip() + '/' + p[36].strip() + ', ' + p[37].strip() + '.' + p[38].strip()
        return
    if len(p) == 37: # In
        # print("Match: " + p[4] + " v " + p[23])
        # print("Details: " + p[4], p[8], p[9] + '.' + p[10], p[13], p[14] + '.' + p[15], p[23], p[26], p[27] + '.' + p[28], p[31] + '/' + p[32], p[33])
        eachRowData[0] = p[4].strip() + " v " + p[23].strip()
        eachRowData[2] = p[4].strip() + ', ' + p[8].strip() + ', ' + p[9].strip() + '.' + p[10].strip() + ', ' + p[13].strip() + ', ' + p[14].strip() + '.' + p[15].strip() + ', ' + p[23].strip() + ', ' + p[26].strip() + ', ' + p[27].strip() + '.' + p[28].strip() + ', ' + p[31].strip() + '/' + p[32].strip() + ', ' + p[33].strip()
        return
    if len(p) == 33: # In
        # print("Match: " + p[4] + " v " + p[23])
        # print("Details: " + p[4], p[8], p[9] + '.' + p[10], p[13] + '/' +  p[14], p[15], p[23], p[26], p[27] + '.' + p[28])
        eachRowData[0] = p[4].strip() + " v " + p[23].strip()
        eachRowData[2] = p[4].strip() + ', ' + p[8].strip() + ', ' + p[9].strip() + '.' + p[10].strip() + ', ' + p[13].strip() + '/' + p[14].strip() + ', ' + p[15].strip() + ', ' + p[23].strip() + ', ' + p[26].strip() + ', ' + p[27].strip() + '.' + p[28].strip()
        return
    if len(p) == 38: # In
        # print("Match: " + p[4] + " v " + p[23])
        # print("Details: " + p[4], p[8], p[9] + '.' + p[10], p[13], p[14] + '.' + p[15], p[23], p[26] + '/' + p[27], p[32] + '.' + p[33])
        eachRowData[0] = p[4].strip() + " v " + p[23].strip()
        eachRowData[2] = p[4].strip() + ', ' + p[8].strip() + ', ' + p[9].strip() + '.' + p[10].strip() + ', ' + p[13].strip() + ', ' + p[14].strip() + '.' + p[15].strip() + ', ' + p[23].strip() + ', ' + p[26] + '/' + p[27] + ', ' + p[32].strip() + '.' + p[33].strip()
        return
    if len(p) == 40: # In for two rules # Issue is 9
        # print("Match: " + p[4] + " v " + p[26])
        # print("Details: " + p[4], p[8], p[9] , p[12] + '/' + p[13], p[18],  p[26], p[29], p[30] + '.' + p[31], p[34] + '/' + p[35], p[36])
        eachRowData[0] = p[4].strip() + " v " + p[26].strip()
        eachRowData[2] = p[4].strip() + ', ' + p[8].strip() + ', ' + p[9].strip() + ', ' + p[12].strip() + '/' + p[13].strip() + ', ' + p[18].strip() + ', ' + p[26].strip() + ', ' + p[29].strip() + ', ' + p[30].strip() + '.' + p[31].strip() + ', ' + p[34].strip() + '/' + p[35].strip() + ', ' + p[36].strip()
        return
    if len(p) == 23: # In
        # print("Match: " + p[4] + " v " + p[16])
        # print("Details: " + p[4], p[16])
        eachRowData[0] = p[4].strip() + " v " + p[16].strip()
        eachRowData[2] = p[4].strip() + ', ' + p[16].strip()
        return
    if len(p) == 17 and "href" not in p[3]: # In
        # print("Match: " + p[3] + " v " + p[11])
        # print("Details: " + p[3], p[11])
        eachRowData[0] = p[3].strip() + " v " + p[11].strip()
        eachRowData[2] = p[3].strip() + ', ' + p[11].strip()
        return

    #For right table
    if len(p) == 26: # In
        # print("Result and Venue: " + p[4], p[7], p[11])
        eachRowData[3] = p[4].strip() + ', ' + p[7].strip() + ', ' + p[11].strip()
        parsedData.append(eachRowData)
        return
    if len(p) == 27: # In
        # print("Result and Venue: " + p[4], p[7], p[8], p[12])
        eachRowData[3] = p[4].strip() + ', ' + p[7].strip() + p[8].strip() + p[9].strip() + ', ' + p[12].strip()
        parsedData.append(eachRowData)
        return
    if len(p) == 20: # In
        # print("Result and Venue: " + p[4] + ", " + p[7] + ", " + p[11])
        eachRowData[3] = p[4].strip() + ', ' + p[7].strip() + ', ' + p[11].strip()
        parsedData.append(eachRowData)
        return
    if len(p) == 24: # In
        # print("Result and Venue: " + p[4] + ", " + p[7] + ", " + p[11])
        eachRowData[3] = p[4].strip() + ', ' + p[7].strip() + ', ' + p[11].strip()
        parsedData.append(eachRowData)
        return
    if len(p) == 25: # In
        # print("Result and Venue: " + p[4] + ", " + p[7] + ", " + p[11])
        eachRowData[3] = p[4].strip() + ', ' + p[7].strip() + ', ' + p[11].strip()
        parsedData.append(eachRowData)
        return
    if len(p) == 19: # In
        # print("Result and Venue: " + p[4] + ", " + p[7] + ", " + p[12])
        eachRowData[3] = p[4].strip() + ', ' + p[7].strip() + ', ' + p[12].strip()
        parsedData.append(eachRowData)
        return
    if len(p) == 22:
        # print("Result and Venue: " + p[4] + ", " + p[7] + p[8] + p[9], p[13])
        eachRowData[3] = p[4].strip() + ', ' + p[7].strip() + p[8].strip() + p[9].strip() + ', ' + p[13].strip()
        parsedData.append(eachRowData)
        return
    if len(p) == 13:
        # print("Result and Venue: " + p[4] + ", " + p[8] + ", Yet to take place")
        eachRowData[3] = p[4].strip() + ', ' + p[8].strip() + ', Yet to take place'
        parsedData.append(eachRowData)
        return
    if len(p) == 17 and "/td" not in p[6]:
        # print("Result and Venue: " + p[4] + p[5] + p[6] + p[7] + p[8] , p[12])
        eachRowData[3] = p[4].strip() + p[5].strip() + p[6].strip() + p[7].strip() + p[8].strip() + ', ' + p[12].strip()
        parsedData.append(eachRowData)
        return
    if len(p) == 14:
        # print("Result and Venue: " + p[4] + p[5] , p[9] + ", Yet to take place")
        eachRowData[3] = p[4].strip() + p[5].strip() + ', ' + p[9].strip() + ', Yet to take place'
        parsedData.append(eachRowData)
        return
    if len(p) == 6:
        # print("Result and Venue: Yet to take place")
        eachRowData[3] = "Yet to take place"
        parsedData.append(eachRowData)
        return

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
        file_obj= open('webpage.html','r',encoding="utf-8")
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

    # print parsed data
    # for i in range(len(parsedData)):
    #     print(parsedData[i])
    #     print('\n')
    # print(parsedData)

    # write parsed data to file
    try:
        file_obj = open('parsedData.txt', 'w')
        for i in range(len(parsedData)):
            # Writing each data of list seperated by '|'
            file_obj.write('|'.join(parsedData[i]))
            file_obj.write('\n')
        file_obj.close()
    except:
        print("Error opening file 'parsedData.txt'")
        return


if __name__ == '__main__':
    main()
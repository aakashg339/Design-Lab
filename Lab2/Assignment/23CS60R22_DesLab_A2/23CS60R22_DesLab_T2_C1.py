import ply.lex as lex
import ply.yacc as yacc
import re

## For Medal Table

###DEFINING TOKENS###
tokens = ('BEGINTABLE', 
'OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF',
'CONTENT', 'OPENDATA', 'CLOSEDATA' ,'OPENSPAN',
'CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 'OPENSTYLE', 'CLOSESTYLE','GARBAGE')
t_ignore = '\t'

###############Tokenizer Rules################
def t_BEGINTABLE(t):
     r'<caption>2020.Summer.Olympics.medal.table<sup.id="cite_ref-227".class="reference"><a.href="\#cite_note-227">&\#91;219&\#93;</a></sup></caption>'
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
index = 0
medalData = []
dataEachRow = []

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
                    | OPENHEADER OPENHREF CONTENT CLOSEHREF CLOSEHEADER handleheader
                    | OPENHEADER CONTENT OPENHREF CONTENT CLOSEHREF CLOSEHEADER dataCell
                    | empty'''
    
    global dataEachRow
    if len(p) == 8:
       # Extracting the href part using regex. Below is the pattern used
        #<a href="/wiki/Australia_at_the_2020_Summer_Olympics" title="Australia at the 2020 Summer Olympics">
        #print("NOC: ", p[4])
        dataEachRow.append(p[4])

def p_dataCell(p):
    '''dataCell : OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA dataCell
    		| OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA dataCell
                | OPENDATA CONTENT CLOSEDATA handleheader
                | OPENDATA CONTENT CLOSEDATA dataCell
                | OPENDATA CLOSEDATA dataCell
                | empty''' 
    global index
    global dataEachRow
    if len(p) == 5 and index == 0:
        #print("Total: ", p[2])
        dataEachRow.append(int(p[2]))
        index = index + 1
        return
    if len(p) == 5 and index == 1:
        #print("Bronze: ", p[2])
        dataEachRow.append(int(p[2]))
        index = index + 1
        return
    if len(p) == 5 and index == 2:
        #print("Silver: ", p[2])
        dataEachRow.append(int(p[2]))
        index = index + 1
        return
    if len(p) == 5 and index == 3:
        #print("Gold: ", p[2])
        dataEachRow.append(int(p[2]))
        index = index + 1
        return
    if len(p) == 5 and index == 4:
        #print("Rank: ", p[2])
        dataEachRow.append(int(p[2]))
        medalData.append(dataEachRow)
        dataEachRow = []
        index = 0
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

#########Helper Functions########
def printMedalData():
    # Printing data in format <Rank>    <Country>    <Gold>    <Silver>    <Bronze>    <Total>, such that data appears as columns
    print("Rank\t\tCountry\tGold\tSilver\tBronze\tTotal")
    for i in range(len(medalData)):
        if len(medalData[i][4]) > 7:
            print(str(medalData[i][4])+'\t'+str(medalData[i][5])+'\t'+str(medalData[i][3])+'\t'+str(medalData[i][2])+'\t'+str(medalData[i][1])+'\t'+str(medalData[i][0]))
        else:
            print(str(medalData[i][4])+'\t\t'+str(medalData[i][5])+'\t'+str(medalData[i][3])+'\t'+str(medalData[i][2])+'\t'+str(medalData[i][1])+'\t'+str(medalData[i][0]))

def writingDataToFile():
    # Writing medal data in a file. Data writting in format <country name>:<rank>,<gold>,<silver>,<bronze>,<total>
    try:
        file_obj = open('medalData.txt','w',encoding="utf-8")
        for i in range(len(medalData)):
            file_obj.write(str(medalData[i][4])+':'+str(medalData[i][5])+','+str(medalData[i][3])+','+str(medalData[i][2])+','+str(medalData[i][1])+','+str(medalData[i][0])+'\n')
        file_obj.close()
    except:
        print("Not able to write data for file medalData.txt")
        return

    # Writing country list in a file
    try:
        file_obj = open('countryList.txt','w',encoding="utf-8")
        for i in range(len(medalData)):
            file_obj.write(str(medalData[i][4])+'\n')
        file_obj.close()
    except:
        print("Not able to write data for file countryList.txt")
        return

#########DRIVER FUNCTION#######
def main():
    try:
        file_obj= open('webpage.html','r',encoding="utf-8")
        data=file_obj.read()
        file_obj.close()
        lexer = lex.lex()
        lexer.input(data)
        # file_obj = open('tokens.txt','w',encoding="utf-8")
        # for tok in lexer:
        #     # print(tok)
        #     file_obj.write(str(tok)+'\n')
        # file_obj.close()
        parser = yacc.yacc()
        parser.parse(data)
        printMedalData()
        writingDataToFile()
    except:
        print("Not able to read data from file webpage.html")
        return

if __name__ == '__main__':
    main()
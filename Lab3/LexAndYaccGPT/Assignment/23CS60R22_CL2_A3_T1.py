import ply.lex as lex
import ply.yacc as yacc

# Scrapping history and current status of team

###DEFINING TOKENS###
tokens = ('BEGINTABLE', 'ENDTABLE', 
'OPENTABLE', 'CLOSETABLE', 'OPENROW', 'CLOSEROW',
'OPENHEADER', 'CLOSEHEADER', 'OPENHREF', 'CLOSEHREF',
'CONTENT', 'OPENDATA', 'CLOSEDATA' ,'OPENSPAN', 'PTAGOPEN', 'PTAGCLOSE',
'CLOSESPAN', 'OPENDIV', 'CLOSEDIV', 'OPENSTYLE', 'CLOSESTYLE','GARBAGE')
t_ignore = '\t'

###############Tokenizer Rules################
def t_BEGINTABLE(t):
     r'<a.href="/wiki/Cricket_clothing_and_equipment".title="Cricket.clothing.and.equipment">kit</a>'
     return t

def t_ENDTABLE(t):
    # <a href="/wiki/List_of_cricket_grounds_in_[Some other text resolved using regex]" title="List of cricket grounds in [Some other text resolved using regex]">List of cricket grounds in [Some other text resolved using regex]</a>
    r'<a.href="/wiki/List_of_cricket_grounds_in_'
    return t

def t_PTAGOPEN(t):
    r'<p[^>]*>'
    return t

def t_PTAGCLOSE(t):
    r'</p[^>]*>'
    return t

def t_CLOSETAG(t):
    r'</p[^>]*>'
    return t

def t_OPENTABLE(t):
    r'<tbody[^>]*>'
    #return t

def t_CLOSETABLE(t):
    r'</tbody[^>]*>'
    #return t

def t_OPENROW(t):
    r'<tr[^>]*>'
    #return t

def t_CLOSEROW(t):
    r'</tr[^>]*>'
    #return t

def t_OPENHEADER(t):
    r'<th[^>]*>'
    #return t

def t_CLOSEHEADER(t):
    r'</th[^>]*>'
    #return t

def t_OPENHREF(t):
    r'<a[^>]*>'
    #return t

def t_CLOSEHREF(t):
    r'</a[^>]*>'
    #return t

def t_OPENDATA(t):
    r'<td[^>]*>'
    #return t

def t_CLOSEDATA(t):
    r'</td[^>]*>'
    #return t

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
historyAndCurrentStatus = []
currentContent = []

def p_start(p):
    '''start : table'''
    p[0] = p[1]

def p_skiptag(p):
    '''skiptag : CONTENT skiptag
               | OPENHREF skiptag
               | CLOSEHREF skiptag
               | PTAGCLOSE skiptag
               | empty'''

def p_handleheader(p):
    '''handleheader : OPENHEADER CONTENT CLOSEHEADER handleheader
                    | empty'''
    #if len(p) == 5:
    #    print("Header: ", p[2])

def p_dataCell(p):
    '''dataCell : CONTENT dataCell
                | empty
                 '''
    global historyAndCurrentStatus
    global currentContent
    if len(p) == 3:
        currentContent.append(p[1])
    
    if len(p) == 2:
        historyAndCurrentStatus.append(currentContent)
        currentContent = []

def p_handlerow(p):
    
    
    '''handlerow : PTAGOPEN dataCell PTAGCLOSE skiptag handlerow
                | empty'''
    
    global historyAndCurrentStatus
    global currentContent
    
    currentContent = []


def p_table(p):
    '''table : BEGINTABLE skiptag handlerow ENDTABLE '''

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
    global historyAndCurrentStatus

    historyAndCurrentStatus = []

    try:
        file_obj= open('webpage.html','r',encoding="utf-8")
        data=file_obj.read()
        file_obj.close()
    except:
        print("Error. Unable to find webpage.html")
    lexer = lex.lex()
    lexer.input(data)

    # # Writing tokens to file
    # file_obj = open('tokens.txt', 'w')
    # for tok in lexer:
    #     # print(tok)
    #     file_obj.write(str(tok))
    #     file_obj.write('\n')
    # file_obj.close()
    
    
    parser = yacc.yacc()
    parser.parse(data)

    # Reverse each list in historyAndCurrentStatus and combine them to get the text
    parsedText = ""

    for i in range(len(historyAndCurrentStatus)):
        # Checking whether list is empty
        if len(historyAndCurrentStatus[i]) == 0:
            continue
        
        temp = ""
        # Combining the words in the list in reverse order
        for j in range(len(historyAndCurrentStatus[i])-1, -1, -1):
            temp += historyAndCurrentStatus[i][j]
            temp += " "

        # print(temp)
        # print("-------------------------------------------------------------------------")

        parsedText += temp
        parsedText += "\n"

    # Writing the string in file input.txt
    try:
        file_obj = open('input.txt', 'w')
        file_obj.write(parsedText)
        file_obj.close()
    except:
        print("Error. Unable to write to input.txt")
        return    
    
    # print(parsedText)

if __name__ == '__main__':
    main()
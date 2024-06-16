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
     r'<table.class="infobox.vevent".style="width:24em"'
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
sports = []
current_sport = ''

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
                    | OPENHEADER CONTENT CONTENT CLOSEHEADER handleheader
                    | OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER handleheader
                    | OPENHEADER CONTENT CLOSEHEADER dataCell
                    | OPENHEADER CONTENT CONTENT CLOSEHEADER dataCell
                    | OPENHEADER OPENHREF CONTENT CLOSEHREF CONTENT CLOSEHEADER dataCell
                    | empty'''
    # if len(p) == 5:
    #    print("Header: ", p[2])

def p_dataCell(p):
    '''dataCell : OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA dataCell
    		    | OPENDATA CONTENT OPENHREF CONTENT CLOSEHREF CLOSEDATA dataCell
                | OPENDATA CONTENT CLOSEDATA dataCell
                | OPENDATA CLOSEDATA dataCell
                | OPENDATA CONTENT CONTENT CLOSEDATA dataCell
                | OPENDATA CONTENT CONTENT CONTENT CONTENT CONTENT CLOSEDATA dataCell
                | OPENDATA OPENHREF CONTENT CONTENT CLOSEHREF CLOSEDATA dataCell
                | empty'''
    
    global index
    global current_sport
    if len(p) == 5 and p[2].isdigit() and index == 2:
        print("Number of events: ", p[2])
        index = 3
        if current_sport == 'Field_hockey':
            index = 0
        return
    if len(p) == 6 and index == 1:
        print("Dates: ", p[2], '-', p[3])
        index = 2
        return
    if len(p) == 7 and index == 0:
        print("Venue: ", p[3])
        index = 1
        return
    # p[3] does not contain href element
    if len(p) == 8 and index == 0:
        if p[3].find('href') == -1:
            print("Venue: ", p[3], p[4])
        else:
            print("Venue: ", p[2], p[4])
        index = 1
        return
    if len(p) == 9 and index == 3:
        print("Competitors: ", p[2], p[4], p[6])
        index = 0
        return
    if len(p) == 5 and index == 3:
        print("Competitors: ", p[2])
        index = 0
        return
    if len(p) == 6 and index == 3:
        print("Competitors: ", p[2], p[3])
        index = 0
        return

def p_dataCellIgnore(p):
    '''dataCellIgnore : OPENDATA OPENHREF CLOSEHREF CLOSEDATA dataCellIgnore
                |   empty'''
    pass

def p_handlerow(p):
    '''handlerow : OPENROW handleheader CLOSEROW handlerow 
                 | OPENROW dataCell CLOSEROW handlerow
                 | OPENROW dataCellIgnore CLOSEROW handlerow
                 | empty'''
    print("-> handlerow")

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
    # Reading the file sports.txt and storing the list of sports in a list
    global sports
    global current_sport
    sports = []

    try:
        file_obj = open('sports.txt','r',encoding="utf-8")
        for line in file_obj:
            sports.append(line.strip())
        file_obj.close()
    except:
        print("File not found: sports.txt")
        return

    # Reading the html files of the sports and storing the data as string in list
    data = []
    for sport in sports:
        # Error handling for missing files
        try:
            file_obj = open('sports/'+sport+'.html','r',encoding="utf-8")
        except:
            print("File not found: ", sport)
            return
        data.append(file_obj.read())
        file_obj.close()
    
    # For each sport, parsing the data using the parser
    for i in range(len(sports)):
        print("--------------------------Sport: ", sports[i], "----------------------------------")
        current_sport = sports[i]
        lexer = lex.lex()
        lexer.input(data[i])
        # # Writing tokens to a file
        # file_obj = open('tokens.txt','w',encoding="utf-8")
        # for tok in lexer:
        #     file_obj.write(str(tok)+'\n')
        # file_obj.close()
        parser = yacc.yacc()
        parser.parse(data[i])

if __name__ == '__main__':
    main()
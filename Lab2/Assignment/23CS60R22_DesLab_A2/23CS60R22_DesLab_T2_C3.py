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
     r'<table.class="wikitable".style="font-size:85%;.float:right;.text-align:center">|<table.class="wikitable".style="font-size:85%">|<table.class="wikitable".style="font-size:85%;">|<table.class="wikitable".style="font-size:85%;.float:right;">'     
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
multipleMedalWinner = {}
currentData = []
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
                    | OPENHEADER CONTENT CLOSEHEADER dataCell
                    | empty'''

def p_dataCell_empty(p):
    '''dataCell_empty : empty'''

def p_dataCell(p):
    # | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA dataCell_empty
    '''dataCell : OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA dataCell_empty
                    | OPENDATA OPENHREF CONTENT CONTENT CLOSEHREF CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA dataCell_empty
                    | OPENDATA OPENHREF CONTENT CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA dataCell_empty
                    | OPENDATA OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA OPENDATA CONTENT CLOSEDATA dataCell_empty
                    | OPENDATA CLOSEDATA dataCell
                    | OPENDATA CONTENT CLOSEDATA dataCell
                    | OPENDATA CLOSEDATA handleheader
                    | empty'''
    global currentData
    eachData = []
    if len(p) == 19:
        eachData.append(p[3])
        eachData.append(p[7])
        currentData.append(eachData)
        #print(p[3], p[7], p[10], p[13], p[16])
    if len(p) == 23:
        eachData.append(p[3]+p[4])
        eachData.append(p[8])
        currentData.append(eachData)
        #print(p[3], p[4],p[8],p[11],p[14],p[17],p[20])
    if len(p) == 24:
        eachData.append(p[3])
        eachData.append(p[8])
        currentData.append(eachData)
        #print(p[3],p[8],p[12],p[15],p[18],p[21])
    if len(p) == 25:
        eachData.append(p[3]+p[4])
        eachData.append(p[9])
        currentData.append(eachData)
        #print(p[3], p[4],p[9],p[13],p[16],p[19],p[22])
    if len(p) == 26:
        eachData.append(p[3]+p[4]+p[5])
        eachData.append(p[10])
        currentData.append(eachData)
        #print(p[3], p[4], p[5], p[10], p[14], p[17], p[20], p[23])

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
    global currentData
    global multipleMedalWinner

    # Get the list of countries from the file countryList.txt
    countries = []
    with open('countryList.txt','r',encoding="utf-8") as f:
        for line in f:
            countries.append(line.strip())
    
    # Few country names might have spaces in them. Replace them with '_' and create another list
    countries_seperated = []
    for country in countries:
        countries_seperated.append(country.replace(' ','_'))

    # For each country, parse the html file and extract the data
    for i, country in enumerate(countries_seperated):
        file_obj = open('countries/'+country+'.html','r',encoding="utf-8")
        data = file_obj.read()
        file_obj.close()

        #print("Country: ", country)

        # Build the lexer
        lexer = lex.lex()
        lexer.input(data)

        # # Write the tokens to a file
        # file_obj = open('tokens.txt','w',encoding="utf-8")
        # for tok in lexer:
        #     # print(tok)
        #     file_obj.write(str(tok)+'\n')
        # file_obj.close()

        currentData = []
        # Build the parser
        parser = yacc.yacc()
        parser.parse(data)

        # Collecting data for each country
        multipleMedalWinner[countries[i]] = currentData

    #print(multipleMedalWinner)
    
    # Writing data to file, by taking only the first 2 cells of the list as we do not need medals informations
    try:
        file_obj = open('multipleMedalWinner.txt','w',encoding="utf-8")
        for key in multipleMedalWinner.keys():
            file_obj.write(key+':')
            for i in range(len(multipleMedalWinner[key])):
                file_obj.write(multipleMedalWinner[key][i][0]+',')
                # If we are at last cell then do not add | , else add | to seperate the cells
                if i == len(multipleMedalWinner[key])-1:
                    file_obj.write(multipleMedalWinner[key][i][1])
                else:
                    file_obj.write(multipleMedalWinner[key][i][1]+' | ')
            file_obj.write('\n')
        file_obj.close()
    except:
        print("Not able to write data for file multipleMedalWinner.txt")
        return

if __name__ == '__main__':
    main()
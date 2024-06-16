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
     r'<table.class="infobox.vevent".style="width:.25em;">'
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
flagBearer = {}
currentData = []

def p_start(p):
    '''start : handleheader'''
    p[0] = p[1]

def p_skiptag(p):
    '''skiptag : CONTENT skiptag
               | OPENHREF skiptag
               | CLOSEHREF skiptag
               | empty'''

def p_empty(p):
    '''empty :'''
    pass

def p_handleheader(p):
    '''handleheader : OPENHEADER OPENHREF CONTENT CONTENT CONTENT CONTENT CLOSEHREF CLOSEHEADER dataCell
    '''
    # if len(p) == 5:
    #    print("Header: ", p[2])

def p_dataCell_empty(p):
    '''dataCell_empty : empty'''

def p_dataCell(p):
    '''dataCell : OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA dataCell_empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CLOSEHREF CLOSEDATA dataCell_empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA dataCell_empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF OPENHREF CONTENT CONTENT CONTENT CLOSEHREF OPENHREF CONTENT CONTENT CONTENT CLOSEHREF CLOSEDATA dataCell_empty
                | OPENDATA OPENHREF CONTENT CLOSEHREF CLOSEDATA dataCell_empty
                | empty'''
    
    global currentData
    if len(p) == 10:
        currentData.append(p[3]+","+p[6])
        #print("Flag bearers (opening): ", p[3], "," ,p[6])
    if len(p) == 15:
        currentData.append(p[3]+","+p[6])
        #print("Flag bearers (opening): ", p[3], "," ,p[6])
    if len(p) == 17:
        currentData.append(p[3]+","+p[6]+p[7]+p[8])
        #print("Flag bearers (opening): ", p[3], "," ,p[6]+p[7]+p[8])
    if len(p) == 7:
        currentData.append(p[3])
        # print("Flag bearer (closing): ", p[3])
    if len(p) == 12:
        currentData.append(p[3])
        # print("Flag bearer (closing): ", p[3])

def p_error(p):
    pass

#########DRIVER FUNCTION#######
def main():
    global currentData
    global flagBearer

    # Get the list of countries from the file countryList.txt
    countries = []
    try:
        with open('countryList.txt','r',encoding="utf-8") as f:
            for line in f:
                countries.append(line.strip())
    except:
        print("Not able to read data from file countryList.txt")
        exit()
    
    # Few country names might have spaces in them. Replace them with '_' and create another list
    countries_seperated = []
    for country in countries:
        countries_seperated.append(country.replace(' ','_'))

    # For each country, parse the html file and extract the data
    for i, country in enumerate(countries_seperated):
        try:
            file_obj = open('countries/'+country+'.html','r',encoding="utf-8")
            data = file_obj.read()
            file_obj.close()
        except:
            print("Not able to read data from file ", country)
            continue

        # Build the lexer
        lexer = lex.lex()
        lexer.input(data)

        #print("Country", country)

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

        # Collecting data
        flagBearer[countries[i]] = currentData
    
    # Writing data to file
    try:
        file_obj = open('flagBearer.txt','w',encoding="utf-8")
        for country in countries:
            file_obj.write(country+':')
            for i in range(len(flagBearer[country])):
                if i == len(flagBearer[country])-1:
                    file_obj.write(flagBearer[country][i])
                else:
                    file_obj.write(flagBearer[country][i]+',')
            file_obj.write('\n')
        file_obj.close()
    except:
        print("Not able to write data for file flagBearer.txt")
        return

if __name__ == '__main__':
    main()
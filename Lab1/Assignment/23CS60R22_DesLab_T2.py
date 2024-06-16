import ply.lex as lex
import ply.yacc as yacc
import sys
import nltk
from nltk.corpus import brown

havingLexicalError = False
havingSyntaxError = False
NUMBER_OF_WORDS = 100

# NLTK part
nltk.download('brown')
brown_words = brown.words()

article_words = set()
verb_words = set()
verbex_words = set()
noun_words = set()
adj_words = set()

# Getting the words from brown corpus
for (word, tag) in brown.tagged_words():

    if len(article_words) == NUMBER_OF_WORDS and len(verb_words) == NUMBER_OF_WORDS and len(verbex_words) == NUMBER_OF_WORDS and len(noun_words) == NUMBER_OF_WORDS:
        break
    
    if tag == 'AT' and len(article_words) < NUMBER_OF_WORDS:
        article_words.add(word.lower())
    elif tag == 'VB' and len(verb_words) < NUMBER_OF_WORDS:
        verb_words.add(word.lower())
    elif tag in ['BEZ', 'BED', 'BER', 'BEM'] and len(verbex_words) < NUMBER_OF_WORDS:
        verbex_words.add(word.lower())
    elif tag in ['NN', 'NNS', 'NP', 'NPS'] and len(noun_words) < NUMBER_OF_WORDS:
        noun_words.add(word.lower())
    elif tag in ['JJ'] and len(adj_words) < NUMBER_OF_WORDS:
        adj_words.add(word.lower())

# Adding few values to make the sentences in the assignment run
article_words.update(['a', 'an', 'the'])
noun_words.update(['cat'])


# print(r'(' + '|'.join(article_words) + ')')
# print(r'(' + '|'.join(verb_words) + ')')
# print(r'(' + '|'.join(verbex_words) + ')')
# print(r'(' + '|'.join(noun_words) + ')')
# print(r'(' + '|'.join(adj_words) + ')')

# Lexical part
# List of tokens
tokens = [
    'noun',
    'verb',
    'article',
    'adj',
    'verbca',
    'verbcb',
]

# Regular expression rules for simple tokens
t_noun = r'(' + '|'.join(noun_words) + ')'
t_verb = r'(' + '|'.join(verb_words) + ')'
t_article = r'(' + '|'.join(article_words) + ')'
t_adj = r'(' + '|'.join(adj_words) + ')'
t_verbca = r'(is|am|was|were|are)'
t_verbcb = r'(sleeping|talking|crying|laughing|feeding|eating|bathing|grumbling|loitering|watching)'
t_ignore = r'( |,|.|?|!)'

def t_error(t):
    global havingLexicalError
    # Find the position of the end of the line
    endLinePos = t.lexer.lexdata.find('\n', t.lexer.lexpos)
    if endLinePos == -1:
        # If there's no '\n' (end of line), skip to the end of input
        t.lexer.skip(len(t.lexer.lexdata) - t.lexer.lexpos)
    else:
        # Calculate the number of characters until the end of the line and skip
        charsTillEndLine = endLinePos - t.lexer.lexpos
        t.lexer.skip(charsTillEndLine)
    havingLexicalError = True
    # t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# printing tokens
def printTokens(input_expression):
    lexer.input(input_expression)
    while(True):
        tok = lexer.token()
        if not tok:
            break;
        print(tok.type, end =" ")
    print()

# Syntax part
# Parsing rules  

# Grammer given in assignment
# SENTENCE -> NOUN VERB
# NOUN -> ARTICLE | Noun
# ARTICLE -> a | an | the | epsilon
# VERB -> Noun VERB| VERBEX VERB| Verb
# VERBEX -> is | am | was | were | are

# Grammer changed to remove S/R conflict of ARTICLE -> epsilon
# SENTENCE -> NOUN VERB
# NOUN -> ARTICLE Noun | Noun
# ARTICLE -> a | an | the
# VERB -> NOUN VERB | VERBEX VERB | Verb
# VERBEX -> is | am | was | were | are
    
# Modified grammer to add adjective and verbc
# SENTENCE -> NOUN VERB
# NOUN -> ARTICLE Noun | ARTICLE ADJECTIVE Noun | Noun | ADJECTIVE Noun
# ARTICLE -> a | an | the
# VERB -> NOUN VERB | VERBC VERB | Verb | VERBC
# VERBC -> VERBCA VERBCB
# VERBCA -> is | am | was | were | are
# VERBCB -> sleeping | talking | crying | laughing | feeding | eating | bathing | grumbling | loitering | watching
# ADJECTIVE -> Adj

# precedence = (
#     ('left', 'article', 'noun', 'verb'),
# )

def p_calc(p):
    '''
    calc : SENTENCE
            | empty
    '''
    print(p[1])

# SENTENCE -> NOUN VERB
def p_sentence(p):
    '''
    SENTENCE : NOUN VERB
    '''
    p[0] = (p[1], p[2])

# NOUN -> ARTICLE
def p_article_noun(p):
    '''
    NOUN : ARTICLE noun
    '''
    p[0] = (p[1], p[2])

# NOUN -> ADJECTIVE Noun (Added to improve the grammer)
def p_adjective_noun(p):
    '''
    NOUN : ADJECTIVE noun
    '''
    p[0] = (p[1], p[2])

# NOUN -> ARTICLE ADJECTIVE Noun (Added to improve the grammer)
def p_article_adjective_noun(p):
    '''
    NOUN : ARTICLE ADJECTIVE noun
    '''
    p[0] = (p[1], p[2], p[3])

# NOUN -> noun
def p_noun(p):
    '''
    NOUN : noun
    '''
    p[0] = p[1]

# ARTICLE -> a | an | the | epsilon
def p_article(p):
    '''
    ARTICLE : article
                
    '''
    p[0] = p[1]

# VERB -> Noun VERB| VERBC VERB| Verb
def p_verbb_noun(p):
    '''
    VERB : NOUN VERB
            | VERBC VERB
    '''
    p[0] = (p[1], p[2])

def p_verb_one_symbol(p):
    '''
    VERB : verb
            | VERBC
    '''
    p[0] = p[1]

# verbc -> verbca verbcb
def p_verbc(p):
    '''
    VERBC : verbca verbcb
    '''
    p[0] = (p[1], p[2])

# ADJECTIVE -> Adj (Added to improve the grammer)
def p_adjective(p):
    '''
    ADJECTIVE : adj
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    global havingSyntaxError
    havingSyntaxError = True

parser = yacc.yacc()

# Taking input and making decisions accordingly.
while True:
    # Take input expression from the user
    input_expression = input("user: ")

    if input_expression == "exit":
        sys.exit()

    # Getting the number of words in the input expression
    words = input_expression.split()
    numberOfWords = len(words)

    if numberOfWords < 2 or numberOfWords > 15:
        print("The words in sentence should contian at least 2 words and at most 15 words.")
        continue

    # print the tokens
    printTokens(input_expression)

    if havingLexicalError:
        print("Invalid Matching. Note: The spaces are to be ignored. Having Lexical Error.")
        havingLexicalError = False
    else:
        parser.parse(input_expression)

        if havingSyntaxError:
            print("Invalid Matching. Note: The spaces are to be ignored. Having Syntax Error.")
            havingSyntaxError = False
        else:
            print("Valid Matching. Note: The spaces are to be ignored.")
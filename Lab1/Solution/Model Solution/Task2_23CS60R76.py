import ply.lex as lex
import ply.yacc as yacc
import nltk
import re

# nltk.download('brown')
# nltk.download('universal_tagset')

from nltk.corpus import brown

verb_words = [word.lower() for word, pos in brown.tagged_words() if pos.startswith('VB')]
noun_words = set([word.lower() for word, pos in brown.tagged_words() if (pos.startswith('NN') or pos.startswith('NNS') or pos.startswith('NP') or pos.startswith('NPS'))])

def check_brown_pos_tag(word, posSET):
    tagged_words = brown.tagged_words()
    for w, pos in tagged_words:
        if pos in posSET and w.lower() == word.lower():
            print(pos, w, word)
            return True
    return False

tokens = ['FULL_STOP', 'ARTICLE', 'CONJ', 'HELPINGVERB', 'ADVERB', 'VERBA', 'VERBB', 'NOUN', 'PROPERNOUN', 'PRONOUN']

t_FULL_STOP = r'\.'

def t_ARTICLE(t):
    r'\b(a|an|the)\b'
    t.type = "ARTICLE"
    return t

def t_CONJ(t):
    r'\b(and|or|but)\b'
    t.type = 'CONJ'
    return t

def t_HELPINGVERB(t):
    r'\b(is|am|are|was|were|has|have|had|be)\b'
    return t

def t_ADVERB(t):
    r'\b[a-z]+(?:y)\b'
    return t

def t_VERBA(t):
    r'\b[a-z]+(?:ing)\b'
    return t

def t_VERBB(t):
    r'\b[a-z]+(?:ed|es|s)\b'
    return t

def t_PRONOUN(t):
    r'\bI|you|he|she|it|we|they\b'
    return t

def t_PROPERNOUN(t):
    r'\b[A-Z][a-z]+\b'
    return t

def t_NOUN(t):
    r'\b[a-z]+\b'
    return t

t_ignore = r' '  # Ignore Spaces and Enter

def t_error(t):   # Skip Illegal Characters
    # print("InValid Character found: {}".format(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()

def p_sentence(p):
    '''
    sentence : NP VP fullstop
             | sentence CONJ sentence
    '''
    p[0] = ("START", p[1], p[2], p[3])
    print("\nVALID sentence...")

def p_fullstop(p):
    '''
    fullstop : FULL_STOP
             | 
    '''
    p[0] = '.'

def p_NP(p):
    '''
    NP : ARTICLE NOUN
       | PRONOUN
       | PROPERNOUN
    '''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

def p_VP(p):
    '''
    VP : HELPINGVERB VERBA
       | HELPINGVERB VERBA NP
       | VERBB
       | VERBB NP
       | VP ADVERB
    '''
    if len(p) == 4:
        p[0] = (p[1], p[2], p[3])
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

def p_error(p):
    if not p:
        print("Syntax Error Found @ EOF")
    else:
        print("Syntax Error Found @ {}".format(p.lexpos))
    print("\nInValid sentence....")

parser = yacc.yacc()

def display_lexer_tokens(str_exp):
    while True:
      LToken = lexer.token()
      if not LToken:
         break
      print(LToken)

while(True):
    try:
        print("\nEnter Ctrl+z to EXIT")
        sent = input("Enter Sentence: ")
        lexer.input(sent)
        display_lexer_tokens(sent)
    except EOFError:
        print("BYE-BYE...")
        break
    parser.parse(sent, lexer)
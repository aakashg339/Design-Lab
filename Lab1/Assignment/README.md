# English Language Grammer
This project is part of an Design Lab (CS69202) assignment at IIT Kharagpur.

#### Programming Languages Used
* Python (Version - 3.8.10)

#### Libraries Used
* ply
* sys
* nltk
In case of any missing library, kindly install it using 
- pip3 install < library name > (for Python)
(Some libraries mentioned above come as part of python3)

## TASK 2
We implemented the context free grammer for english language.

## Other Details

#### Grammer used
SENTENCE -> NOUN VERB
NOUN -> ARTICLE Noun | ARTICLE ADJECTIVE Noun | Noun | ADJECTIVE Noun
ARTICLE -> a | an | the
VERB -> NOUN VERB | VERBC VERB | Verb | VERBC
VERBC -> VERBCA VERBCB
VERBCA -> is | am | was | were | are
VERBCB -> sleeping | talking | crying | laughing | feeding | eating | bathing | grumbling | loitering | watching
ADJECTIVE -> Adj

#### Description
Implemented the above grammer

Regex implementation
- For NOUN, ARTICLE, ADJECTIVE, VERB
Took first 100 words of given type(NOUN, ARTICLE, ADJECTIVE, VERB) from nltk brown corpus. 
Used those words in regex passed to the token for the type say noun, verb, etc.
- For verbca, verbcb
Used the words as described in the assignment.

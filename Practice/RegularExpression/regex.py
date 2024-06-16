import re

text_to_search = '''
abcdefghijklmnopqurtuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
1234567890

Ha HaHa

MetaCharacters (Need to be escaped):
. ^ $ * + ? { } [ ] \ | ( )

coreyms.com

321-555-4321
321--555-4321
123.555.1234
123*555*1234
800-555-1234
900-555-1234

Mr. Schafer
Mr Smith
Ms Davis
Mrs. Robinson
Mr. T

cat
mat
pat
bat
'''

sentence = 'Start a sentence and then bring it to an end'

print(r'\tHello')

# pattern = re.compile(r'abc')

# matches = pattern.finditer(text_to_search)

# for match in matches:
#     print(match.span())
#     startIndex = match.span()[0]
#     endIndex = match.span()[1]
#     print(text_to_search[startIndex:endIndex])

# # '.' is treaded as a special character in regex. Use '\.' to match a literal '.'. Ex - r'\.'
# pattern = re.compile(r'coreyms\.com')

# matches = pattern.finditer(text_to_search)

# for match in matches:
#     print(match)

# # for digit matching
# pattern = re.compile(r'\d')

# matches = pattern.finditer(text_to_search)

# for match in matches:
#     print(match)

# # for word boundary matching
# pattern = re.compile(r'\bHa')

# matches = pattern.finditer(text_to_search)

# for match in matches:
#     print(match)

# # for matching the start of the string
# pattern = re.compile(r'^Start')
# matches = pattern.finditer(sentence)
# for match in matches:
#     print(match)

# # for matching the end of the string
# pattern = re.compile(r'end$')
# matches = pattern.finditer(sentence)
# for match in matches:
#     print(match)

# # For matching numbers
# pattern = re.compile(r'\d\d\d.\d\d\d.\d\d\d\d')
# matches = pattern.finditer(text_to_search)
# for match in matches:
#     print(match)
# or to matc only '.' or '-' use
# pattern = re.compile(r'\d\d\d[-.]\d\d\d[-.]\d\d\d\d')
# matches = pattern.finditer(text_to_search)
# for match in matches:
#     print(match)
# or below to match '--'
# pattern = re.compile(r'\d\d\d[-.]+\d\d\d[-.]\d\d\d\d')
# matches = pattern.finditer(text_to_search)
# for match in matches:
#     print(match)
# To match numbers 800 or 900
# pattern = re.compile(r'[89]00[-.]\d\d\d[-.]\d\d\d\d')
# matches = pattern.finditer(text_to_search)
# for match in matches:
#     print(match)
# TO match numbers between 1 to 5
# pattern = re.compile(r'[1-5]')
# matches = pattern.finditer(text_to_search)
# for match in matches:
#     print(match)



# # For getting phone numbers
# data = ""
# # if there is a problem in decoding then use with open('Reference/data.txt', 'r', encoding='utf-8') as file:
# with open('Reference/data.txt', 'r') as file:
#     data = file.read()
# pattern = re.compile(r'\d{3}-\d{3}-\d{4}')
# matches = pattern.finditer(data)
# for match in matches:
#     print(match)

# # [^ ]    - Matches Characters NOT in brackets
# pattern = re.compile(r'[^a-zA-Z]')
# matches = pattern.finditer(text_to_search)
# for match in matches:
#     print(match)
# Ex - to not match bat bu match cat, mat, pat
# pattern = re.compile(r'[^b]at')
# matches = pattern.finditer(text_to_search)
# for match in matches:
#     print(match)

# # Quantifiers
# pattern = re.compile(r'M[a-z]+\.?\s[A-Z][a-z]*')
# pattern = re.compile(r'M[a-z]+\.?\s[A-Z]\w*')
pattern = re.compile(r'M(r|s|rs)\.?\s[A-Z]\w*')
matches = pattern.finditer(text_to_search)
for match in matches:
    print(match)

# findall() - returns a list of all matches
# Ex - matches = patttern.findall(text_to_search)
# match() - returns the first match
# Ex - match = pattern.match(text_to_search)
# print(match)
# search() - returns a match object if there is a match anywhere in the string
# Ex - match = pattern.search(text_to_search)
# print(match)
    
# Flags
# re.IGNORECASE - Ignore case
# Ex - pattern = re.compile(r'start', re.IGNORECASE)
# matches = pattern.finditer(text_to_search)
# for match in matches:
#     print(match)
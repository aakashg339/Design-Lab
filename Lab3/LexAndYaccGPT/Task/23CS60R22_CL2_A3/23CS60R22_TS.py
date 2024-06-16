import openai
import time

# Reading API key
with open("api_key.txt") as f:
  api_key = f.read()

# Reading input file
with open("input.txt") as f:
  input_passage = f.read()

system_prompt = "You are an AI assistant capable of summarizing a passage."
user_prompt = "\nPassage : " + input_passage
openai.api_key =  api_key# Your key goes here

response = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages=[
    {
    "role": "system",
    "content": system_prompt
    },
    {
    "role": "user",
    "content": user_prompt
    }
    ],

)
# print(response)
# print(response.choices[0]['message']['content'])

# Storing the result in text file
with open("output.txt", 'w+') as f:
  f.write(response.choices[0]['message']['content'])

inputLength = len(input_passage.strip().split())
outputLength = len(response.choices[0]['message']['content'].strip().split())

print("Number of words in input : " + str(inputLength))
print("Number of words in output : " + str(outputLength))

print("Percentage reduction : " + str((((inputLength)/outputLength))))
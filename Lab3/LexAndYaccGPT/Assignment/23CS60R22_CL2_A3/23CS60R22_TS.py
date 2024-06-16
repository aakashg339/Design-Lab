import openai
import time

# Reading API key
with open("api_key.txt") as f:
  api_key = f.read()

# Reading input file
with open("input.txt") as f:
  input_passage = f.read()

# Generating prompt for GPT for 4090 words from input_passage at a time(because of maximum limit of 4097 tokens per request)
# Creating a list of prompts
promptList = []
for i in range(0, len(input_passage), 4090):
  promptList.append(input_passage[i:i+4090])

# Generating response from GPT for each prompt
responseList = []

for prompt in promptList:
  system_prompt = "You are an AI assistant capable of summarizing a passage."
  user_prompt = "\nPassage : " + prompt
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
  responseList.append(response.choices[0]['message']['content'])
  print("Waiting .......... Still waiting ..........")
  time.sleep(30)


# Combining response list into a single string
responseString = " ".join(responseList)

# Storing the result in text file
with open("output.txt", 'w+') as f:
  f.write(responseString)

inputLength = len(input_passage.strip().split())
outputLength = len(responseString.strip().split())
reductionFactor = str((((inputLength)/outputLength)))

# Writing the reduction factor in input.log file
try:
  file_obj = open('input.log', 'a')
  file_obj.write("Reduction Factor: " + reductionFactor + '\n')
  file_obj.close()
except:
  print("Error. Unable to write to input.log")
  exit()
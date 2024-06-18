import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

FILE_INPUT = 'gpt_2_gen_input.txt'
FILE_OUTPUT = 'gpt_2_gen_output.txt'

try:
    # start = time.time()
    # Load pre-trained GPT-2 model and tokenizer
    #model_name = "gpt2"
    model_name = "openai-community/gpt2"  # You can choose from "gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Set device to GPU if available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    # print(device)

    # Generate text based on a prompt (same generate_text() function as before)
    def generate_text(prompt, max_length=80):
        input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
        output = model.generate(input_ids, max_new_tokens = 30, pad_token_id=tokenizer.eos_token_id, no_repeat_ngram_size=3, num_return_sequences=1, top_p = 0.95, temperature = 0.1, do_sample = True)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return generated_text

    # Read the prompt from a text file
    with open(FILE_INPUT, 'r') as f:
        prompt = f.read()

    generated_text = generate_text(prompt)
    # end = time.time()
    # print(f'Time taken = {end - start}')
    # # Print the generated text
    # print("Generated Text:")
    # print('--------------------')
    # print(generated_text)

    # What are my options if my flight gets canceled by the airline? 
    # If you're flying to or from a major airport, you can cancel your flight at any time. If you're traveling to or coming from
    # Kindly just extract the answer from the generated text using python code and print it.

    sentences = generated_text.split('\n')

    # From sentences, concadenate the sentences from index 2 to the end, so it appears as a single sentence
    sentences[2] = ' '.join(sentences[2:])

    # print('Answer:', sentences[2])

    with open(FILE_OUTPUT, 'w') as f:
        f.write(sentences[2])
except:
    errorMessage = 'An error occurred while generating text. Please try again.'

    with open(FILE_OUTPUT, 'w') as f:
        f.write(errorMessage)
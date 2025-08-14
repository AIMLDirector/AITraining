import numpy as np
import pandas as pd
import tensorflow as tf
import warnings
from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline

text= input("Enter your sentence here\n") 
def generate_text(prompt):
    generator = pipeline('text-generation', model='gpt2')
    generated_text = generator(prompt, max_length=200, num_return_sequences=1, truncation=True)

    print(generated_text[0]['generated_text'])
    
generate_text(text)

# manual Implementation
def sort_dicts_manual(lst, key):
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i][key] > lst[j][key]:
                lst[i], lst[j] = lst[j], lst[i]
    return lst





# AI-Suggested Implementation (Hugging Face Transformers Approach)

from transformers import pipeline
import torch

def sort_dicts_transformers(lst, key):
    # Use a text generation model to "reason" about sorting
    sorter = pipeline("text-generation", model="microsoft/DialoGPT-medium")
    
    # Convert to natural language problem
    prompt = f"Sort this list of dictionaries by the '{key}' key: {lst}. Return only the sorted list."
    
    response = sorter(prompt, max_length=500, num_return_sequences=1)
    sorted_result = eval(response[0]['generated_text'].split(":")[-1].strip())
    return sorted_result

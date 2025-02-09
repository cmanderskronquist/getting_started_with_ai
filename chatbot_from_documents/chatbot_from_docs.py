import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import time

# Set up env : source venv/bin/activate

# Read Hugging Face token from file
with open("hf_token", "r") as token_file:
    HF_TOKEN = token_file.read().strip()

# Start URL for recursive web scraping
BASE_URL = "https://support.apple.com/en-gb/guide/mac-help/welcome/mac"
VISITED_URLS = set()

def scrape_text_recursive(url, depth=3):  # Increased depth to capture more pages
    if depth == 0 or url in VISITED_URLS:
        return ""
    
    VISITED_URLS.add(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract text from multiple HTML tags
    text_elements = soup.find_all(["p", "li", "div", "span"])  
    text = " ".join([elem.get_text() for elem in text_elements])
    
    # Find links to other Apple support pages and follow them recursively
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("/en-gb/guide/"):
            full_url = "https://support.apple.com" + href
            text += " " + scrape_text_recursive(full_url, depth - 1)
    
    return text

print("Fetching text from Apple Support...")
document_text = scrape_text_recursive(BASE_URL, depth=3)  # Using new depth
print("Document length:", len(document_text), "characters")

# Create embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
sentences = document_text.split(".")  # Split into sentences
embeddings = model.encode(sentences)

# Create FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

def retrieve_relevant_text(question: str):
    question_embedding = model.encode([question])
    D, I = index.search(np.array(question_embedding), k=3)
    answers = [sentences[i] for i in I[0] if i < len(sentences)]
    return "\n".join(answers)

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1", token=HF_TOKEN)
llm_model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.1", 
    torch_dtype=torch.float16, 
    device_map="auto", 
    token=HF_TOKEN
)

# Optimize for Apple Silicon (Metal GPU acceleration)
device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"

def generate_answer_with_llm(question: str):
    context = retrieve_relevant_text(question)
    prompt = f"""
    Use the following context to answer the question:
    
    Context:
    {context}
    
    Question:
    {question}
    
    Answer:
    """
    
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    output = llm_model.generate(**inputs, max_length=500, do_sample=True, temperature=0.7)
    return tokenizer.decode(output[0], skip_special_tokens=True).strip()

# CLI chatbot
while True:
    question = input("Question: ")
    if question.lower() in ["exit", "quit"]:
        break
    print("Answer:\n", generate_answer_with_llm(question))

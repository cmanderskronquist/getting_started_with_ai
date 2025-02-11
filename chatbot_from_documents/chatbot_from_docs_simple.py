import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# source venv/bin/activate

# 1. Hämta och extrahera text från en Apple-manual (exempel: macOS-manual)
URL = "https://support.apple.com/sv-se/guide/mac-help/welcome/mac"  # Exempel-URL
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Extrahera all text från sidan
document_text = " ".join([p.get_text() for p in soup.find_all("p")])
print("Dokumentets längd:", len(document_text), "tecken")

# 2. Skapa embeddings med SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
sentences = document_text.split(".")  # Dela upp i meningar
embeddings = model.encode(sentences)

# 3. Skapa en FAISS-index för effektiv sökning
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

# 4. Frågebaserad sökning
def answer_question(question: str):
    question_embedding = model.encode([question])
    D, I = index.search(np.array(question_embedding), k=3)
    answers = [sentences[i] for i in I[0]]
    return "\n".join(answers)

# Testa chatboten
while True:
    question = input("Fråga: ")
    if question.lower() in ["exit", "quit"]:
        break
    print("Svar:\n", answer_question(question))

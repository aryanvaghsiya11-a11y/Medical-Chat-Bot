# Medical Chat Bot 🏥🤖

An intelligent, conversational web application designed to assist users with medical and healthcare-related inquiries. This project leverages **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware responses grounded in medical literature.

![image alt](https://github.com/aryanvaghsiya11-a11y/Medical-Chat-Bot/blob/b115b4cdc859776513e5b048dc400aba72d01c03/medical.png)

## ✨ Features

* **Conversational AI:** Powered by Google's `Gemini 2.5 Flash` for fast, intelligent, and concise responses.
* **Context-Aware Memory:** Utilizes a history-aware retriever, allowing the bot to remember previous turns in the conversation for natural follow-up questions.
* **Vector Search:** Integrates **Pinecone** to efficiently store and retrieve high-dimensional embeddings of medical documents.
* **Hugging Face Embeddings:** Converts raw medical text into rich vector representations for accurate semantic search.
* **Web Interface:** A clean, user-friendly frontend served via **Flask**.

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **LLM Orchestration:** LangChain (`langchain_google_genai`, `langchain_classic`)
* **Vector Database:** Pinecone
* **Embeddings:** Hugging Face
* **LLM:** Google Gemini 2.5 Flash

## 🚀 Installation and Setup

# How to run?
### STEPS:

Clone the repository

```bash
Project repo: https://github.com/aryanvaghsiya11-a11y/Medical-Chat-Bot.git
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n medibot python=3.10 -y
```

```bash
conda activate medibot
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


### Create a `.env` file in the root directory and add your Pinecone & openai credentials as follows:

```ini
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OPENAI_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


```bash
# run the following command to store embeddings to pinecone
python store_index.py
```

```bash
# Finally run the following command
python app.py
```

Now,
```bash
open up localhost:
```


### Techstack Used:

- Python
- LangChain
- Flask
- GPT
- Pinecone

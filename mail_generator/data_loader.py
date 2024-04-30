import uuid

import pandas as pd
from langchain_community.document_loaders import SeleniumURLLoader
import re
import chromadb


def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]*?>', '', text)
    # Remove URLs
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s{2,}', ' ', text)
    # Trim leading and trailing whitespace
    text = text.strip()
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text


portfolio_data = pd.read_csv("/home/mind/Documents/projects/mail_generator/mail_generator/cleaned_portfolio.csv",
                             index_col=0).dropna()

client = chromadb.PersistentClient(path="vectorstore")
collection = client.get_or_create_collection(name="portfolios")
if not collection.count():
    for _, row in portfolio_data.iterrows():
        collection.add(documents=row["Technology Platform"],
                       metadatas={"links": row["Link"]},
                       ids=[str(uuid.uuid4())])


class ChromaDBClient:
    """Class to interact with ChromaDB"""
    def __init__(self, path):
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name="portfolios")

    def add_documents(self, documents, metadatas, ids):
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)

    def get_collection(self):
        return self.collection

    def query(self, query_texts, n_results):
        return self.collection.query(query_texts=query_texts, n_results=n_results)


class DataLoader:
    def __init__(self, urls):
        self.loader = SeleniumURLLoader(urls=urls)

    def load_data(self):
        data = self.loader.load()
        return clean_text(data.pop().page_content)

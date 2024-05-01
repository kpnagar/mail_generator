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


class PortfolioData:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path, index_col=0).dropna()

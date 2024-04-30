import uuid
from typing import List, Optional

import pandas as pd

from data_loader import DataLoader, ChromaDBClient
from chains import extract_jobs, write_mail


class PortfolioData:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path, index_col=0).dropna()


class EmailGenerator:
    def __init__(self, chroma_client: ChromaDBClient, portfolio_data: PortfolioData):
        self.chroma_client = chroma_client
        self.portfolio_data = portfolio_data

    def generate_email(self, job: dict) -> str:
        skills = job.get('skills', [])
        links = self.get_relevant_links(skills)
        return write_mail(job, links)

    def get_relevant_links(self, required_skills: List[str]) -> List[dict]:
        query_texts = required_skills if required_skills else ['Software']
        result = self.chroma_client.query(query_texts=query_texts, n_results=3)
        return result.get('metadatas', [])


def main():
    portfolio_file_path = "/home/mind/Documents/projects/mail_generator/mail_generator/cleaned_portfolio.csv"
    urls = ["https://www.mindinventory.com/careers.php"]

    loader = DataLoader(urls=urls)
    chroma_client = ChromaDBClient(path='vectorstore')

    portfolio_data = PortfolioData(file_path=portfolio_file_path)
    email_generator = EmailGenerator(chroma_client, portfolio_data)

    text_data = loader.load_data()
    print(text_data)
    jobs = extract_jobs(text_data)
    print(jobs)

    emails = []
    for job in jobs:
        email = email_generator.generate_email(job)
        emails.append(email)
        print(email)
    print(emails)


if __name__ == '__main__':
    main()
